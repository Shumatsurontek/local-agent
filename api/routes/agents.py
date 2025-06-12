"""
Agent routes for the API
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List
from agents import general_agent, search_agent, finance_agent, code_agent, system_agent
from agents.middleware import track_agent_activity
from api.websocket import manager
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Available agents
AGENTS = {
    "general": general_agent,
    "search": search_agent,
    "finance": finance_agent,
    "code": code_agent,
    "system": system_agent
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
    # Get agent status from WebSocket manager
    agent_statuses = manager.agent_status
    
    agents_info = []
    for agent_id, agent in AGENTS.items():
        status_info = agent_statuses.get(agent_id, {})
        status = status_info.get("status", "unknown")
        
        agents_info.append(AgentInfo(
            id=agent_id,
            name=agent.name,
            description=agent.description or f"{agent.name} agent",
            model=agent.model.id if hasattr(agent.model, 'id') else str(agent.model),
            type=agent_id,
            status=status,
            tools=[tool.__class__.__name__ for tool in agent.tools] if hasattr(agent, 'tools') and agent.tools else [],
            metadata=status_info.get("metadata", {})
        ))
    
    return {
        "agents": [agent.dict() for agent in agents_info]
    }

@router.get("/{agent_id}")
async def get_agent_info(agent_id: str):
    """Get information about a specific agent"""
    if agent_id not in AGENTS:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    
    agent = AGENTS[agent_id]
    return {
        "id": agent_id,
        "name": agent.name,
        "description": agent.description or f"{agent.name} agent",
        "model": agent.model.id if hasattr(agent.model, 'id') else str(agent.model),
        "tools": [tool.__class__.__name__ for tool in agent.tools] if agent.tools else [],
        "instructions": agent.instructions
    }

@track_agent_activity(agent_id="api")
@router.post("/{agent_id}/chat")
async def chat_with_agent(agent_id: str, request: ChatRequest, background_tasks: BackgroundTasks):
    """Chat with a specific agent"""
    if agent_id not in AGENTS:
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
        
        # Update agent status
        manager.update_agent_status(agent_id, {
            "status": "processing",
            "current_task": "chat",
            "message": request.message[:100] + "..." if len(request.message) > 100 else request.message
        })
        
        # Run agent with tracking
        response = await run_agent_with_tracking(agent, agent_id, request.message)
        
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
        
        return ChatResponse(
            agent_id=agent_id,
            agent_name=agent.name,
            response=response.content,
            success=True,
            interaction_id=interaction_id
        )
    except Exception as e:
        logger.error(f"Error in agent {agent_id}: {e}")
        
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
    """Run agent with tracking for WebSocket updates"""
    # This function could be extended to provide step-by-step updates
    # for streaming responses in the future
    return agent.run(message) 