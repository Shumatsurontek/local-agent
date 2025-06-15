"""
Agent routes for the API
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List
from agents import general_agent, search_agent, finance_agent, code_agent, system_agent
from teams import collaborative_team
from agents.middleware import track_agent_activity
from api.websocket import manager
import logging
import time
import json

# Create specific loggers
logger = logging.getLogger(__name__)
ollama_logger = logging.getLogger('ollama')
agent_logger = logging.getLogger('agents')

router = APIRouter()

# Available agents
AGENTS = {
    "general": general_agent,
    "search": search_agent,
    "finance": finance_agent,
    "code": code_agent,
    "system": system_agent,
    "research_team": collaborative_team
}

class ChatRequest(BaseModel):
    message: str
    stream: bool = False
    metadata: Dict[str, Any] = {}

class ChatResponse(BaseModel):
    agent_id: str
    agent_name: str
    response: str
    success: bool
    error: str = None
    metadata: Dict[str, Any] = {}
    interaction_id: str = None

class AgentInfo(BaseModel):
    id: str
    name: str
    description: str
    model: str
    type: str
    status: str
    tools: List[str] = []
    metadata: Dict[str, Any] = {}

@router.get("/")
async def list_agents():
    """List all available agents"""
    agent_logger.info("📋 Listing all available agents")
    
    # Get agent status from WebSocket manager
    agent_statuses = manager.agent_status
    
    agents_info = []
    for agent_id, agent in AGENTS.items():
        status_info = agent_statuses.get(agent_id, {})
        status = status_info.get("status", "unknown")
        
        model_info = agent.model.id if hasattr(agent.model, 'id') else str(agent.model)
        agent_logger.debug(f"🤖 Agent {agent_id}: model={model_info}, status={status}")
        
        agents_info.append(AgentInfo(
            id=agent_id,
            name=agent.name,
            description=agent.description or f"{agent.name} agent",
            model=model_info,
            type=agent_id,
            status=status,
            tools=[tool.__class__.__name__ for tool in agent.tools] if hasattr(agent, 'tools') and agent.tools else [],
            metadata=status_info.get("metadata", {})
        ))
    
    agent_logger.info(f"📋 Found {len(agents_info)} agents")
    return {
        "agents": [agent.dict() for agent in agents_info]
    }

@router.get("/{agent_id}")
async def get_agent_info(agent_id: str):
    """Get information about a specific agent"""
    agent_logger.info(f"ℹ️ Getting info for agent: {agent_id}")
    
    if agent_id not in AGENTS:
        agent_logger.error(f"❌ Agent '{agent_id}' not found")
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    
    agent = AGENTS[agent_id]
    model_info = agent.model.id if hasattr(agent.model, 'id') else str(agent.model)
    
    agent_logger.info(f"✅ Agent {agent_id} info: model={model_info}")
    
    return {
        "id": agent_id,
        "name": agent.name,
        "description": agent.description or f"{agent.name} agent",
        "model": model_info,
        "tools": [tool.__class__.__name__ for tool in agent.tools] if agent.tools else [],
        "instructions": agent.instructions
    }

@track_agent_activity(agent_id="api")
@router.post("/{agent_id}/chat")
async def chat_with_agent(agent_id: str, request: ChatRequest, background_tasks: BackgroundTasks):
    """Chat with a specific agent"""
    start_time = time.time()
    
    agent_logger.info(f"💬 CHAT REQUEST - Agent: {agent_id}")
    agent_logger.info(f"📝 Message: {request.message[:200]}{'...' if len(request.message) > 200 else ''}")
    
    if agent_id not in AGENTS:
        agent_logger.error(f"❌ Agent '{agent_id}' not found")
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    
    # Record interaction in WebSocket
    interaction = {
        "agent_id": agent_id,
        "type": "chat_request",
        "message": request.message,
        "metadata": request.metadata
    }
    manager.record_interaction(interaction)
    
    try:
        agent = AGENTS[agent_id]
        model_info = agent.model.id if hasattr(agent.model, 'id') else str(agent.model)
        
        agent_logger.info(f"🤖 Using agent: {agent.name} with model: {model_info}")
        ollama_logger.info(f"🔄 OLLAMA REQUEST - Model: {model_info}")
        ollama_logger.debug(f"🔧 Agent tools: {[tool.__class__.__name__ for tool in agent.tools] if agent.tools else 'None'}")
        
        # Update agent status
        manager.update_agent_status(agent_id, {
            "status": "processing",
            "current_task": "chat",
            "message": request.message[:100] + "..." if len(request.message) > 100 else request.message
        })
        
        # Run agent with detailed tracking
        ollama_logger.info(f"⚡ Starting Ollama inference...")
        inference_start = time.time()
        
        response = await run_agent_with_tracking(agent, agent_id, request.message)
        
        inference_time = time.time() - inference_start
        ollama_logger.info(f"✅ OLLAMA RESPONSE - Time: {inference_time:.2f}s")
        ollama_logger.debug(f"📤 Response length: {len(response.content)} chars")
        ollama_logger.debug(f"📤 Response preview: {response.content[:300]}{'...' if len(response.content) > 300 else ''}")
        
        # Update agent status
        manager.update_agent_status(agent_id, {
            "status": "idle",
            "last_message": request.message[:100] + "..." if len(request.message) > 100 else request.message,
            "last_response": response.content[:100] + "..." if len(response.content) > 100 else response.content
        })
        
        # Record interaction
        interaction_id = manager.record_interaction({
            "agent_id": agent_id,
            "type": "chat_response",
            "message": request.message,
            "response": response.content,
            "success": True
        })
        
        total_time = time.time() - start_time
        agent_logger.info(f"✅ CHAT SUCCESS - Agent: {agent_id}, Total time: {total_time:.2f}s")
        
        return ChatResponse(
            agent_id=agent_id,
            agent_name=agent.name,
            response=response.content,
            success=True,
            interaction_id=interaction_id
        )
    except Exception as e:
        error_time = time.time() - start_time
        agent_logger.error(f"❌ CHAT ERROR - Agent: {agent_id}, Error: {str(e)}, Time: {error_time:.2f}s")
        ollama_logger.error(f"💥 OLLAMA ERROR: {str(e)}")
        
        # Update agent status
        manager.update_agent_status(agent_id, {
            "status": "error",
            "error": str(e)
        })
        
        # Record error interaction
        interaction_id = manager.record_interaction({
            "agent_id": agent_id,
            "type": "chat_error",
            "message": request.message,
            "error": str(e),
            "success": False
        })
        
        return ChatResponse(
            agent_id=agent_id,
            agent_name=AGENTS[agent_id].name,
            response="",
            success=False,
            error=str(e),
            interaction_id=interaction_id
        )

async def run_agent_with_tracking(agent, agent_id, message):
    """Run agent with detailed tracking for Ollama interactions"""
    agent_logger.debug(f"🔄 Running agent {agent_id} with message: {message[:100]}...")
    
    # Log agent configuration
    model_info = agent.model.id if hasattr(agent.model, 'id') else str(agent.model)
    ollama_logger.debug(f"🔧 Agent config - Model: {model_info}")
    ollama_logger.debug(f"🔧 Agent config - Instructions: {len(agent.instructions)} rules")
    ollama_logger.debug(f"🔧 Agent config - Tools: {[tool.__class__.__name__ for tool in agent.tools] if agent.tools else 'None'}")
    
    try:
        # This is where the actual Ollama call happens
        response = agent.run(message)
        
        # Log response details
        if hasattr(response, 'content'):
            ollama_logger.debug(f"📊 Response type: {type(response).__name__}")
            ollama_logger.debug(f"📊 Response content length: {len(response.content)}")
        
        return response
    except Exception as e:
        ollama_logger.error(f"💥 Agent execution failed: {str(e)}")
        raise 