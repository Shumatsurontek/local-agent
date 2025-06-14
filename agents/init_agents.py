"""
Initialize agents with WebSocket middleware
"""

from agents.general import general_agent
from agents.search import search_agent
from agents.finance import finance_agent
from agents.code import code_agent
from agents.system import system_agent
from agents.middleware import register_agent, track_agent_activity
from teams.collaborative_team import collaborative_team
import logging

logger = logging.getLogger(__name__)

def init_agents():
    """Register all agents with the WebSocket manager"""
    
    # Register General Agent
    register_agent("general", {
        "name": general_agent.name,
        "description": general_agent.description,
        "model": getattr(general_agent.model, "id", "unknown"),
        "type": "general",
        "tools": [t.__class__.__name__ for t in general_agent.tools] if hasattr(general_agent, "tools") and general_agent.tools else []
    })
    
    # Register Search Agent
    register_agent("search", {
        "name": search_agent.name,
        "description": search_agent.description,
        "model": getattr(search_agent.model, "id", "unknown"),
        "type": "search",
        "tools": [t.__class__.__name__ for t in search_agent.tools] if hasattr(search_agent, "tools") and search_agent.tools else []
    })
    
    # Register Finance Agent
    register_agent("finance", {
        "name": finance_agent.name,
        "description": finance_agent.description,
        "model": getattr(finance_agent.model, "id", "unknown"),
        "type": "finance",
        "tools": [t.__class__.__name__ for t in finance_agent.tools] if hasattr(finance_agent, "tools") and finance_agent.tools else []
    })
    
    # Register Code Agent
    register_agent("code", {
        "name": code_agent.name,
        "description": code_agent.description,
        "model": getattr(code_agent.model, "id", "unknown"),
        "type": "code",
        "tools": [t.__class__.__name__ for t in code_agent.tools] if hasattr(code_agent, "tools") and code_agent.tools else []
    })
    
    # Register System Agent
    register_agent("system", {
        "name": system_agent.name,
        "description": system_agent.description,
        "model": getattr(system_agent.model, "id", "unknown"),
        "type": "system",
        "tools": [t.__class__.__name__ for t in system_agent.tools] if hasattr(system_agent, "tools") and system_agent.tools else []
    })
    
    # Register Team
    register_agent("research_team", {
        "name": collaborative_team.name,
        "description": collaborative_team.description,
        "type": "team",
        "members": [
            "search",
            "finance",
            "general"
        ]
    })
    
    logger.info("All agents registered with WebSocket manager")

# Initialize agents on import
init_agents() 