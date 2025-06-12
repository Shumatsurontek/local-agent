"""
Agent routes for the API
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from agents import general_agent, search_agent, finance_agent, code_agent, system_agent

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

class ChatResponse(BaseModel):
    agent_name: str
    response: str
    success: bool
    error: str = None

@router.get("/")
async def list_agents():
    """List all available agents"""
    return {
        "agents": {
            agent_id: {
                "name": agent.name,
                "description": agent.description or f"{agent.name} agent"
            }
            for agent_id, agent in AGENTS.items()
        }
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

@router.post("/{agent_id}/chat")
async def chat_with_agent(agent_id: str, request: ChatRequest):
    """Chat with a specific agent"""
    if agent_id not in AGENTS:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    
    try:
        agent = AGENTS[agent_id]
        response = agent.run(request.message)
        
        return ChatResponse(
            agent_name=agent.name,
            response=response.content,
            success=True
        )
    except Exception as e:
        return ChatResponse(
            agent_name=AGENTS[agent_id].name,
            response="",
            success=False,
            error=str(e)
        ) 