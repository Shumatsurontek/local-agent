"""
Agent middleware for WebSocket notifications
"""

from typing import Dict, Any, Callable, Optional, List
import inspect
import asyncio
import functools
from api.websocket import manager
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def track_agent_activity(agent_id: str):
    """
    Decorator to track agent activity and send updates to WebSocket
    
    Args:
        agent_id: The ID of the agent
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Record start of activity
            start_time = datetime.now()
            
            # Update agent status to "busy"
            manager.update_agent_status(agent_id, {
                "status": "busy",
                "current_task": func.__name__,
                "started_at": start_time.isoformat()
            })
            
            # Record interaction start
            interaction_id = manager.record_interaction({
                "agent_id": agent_id,
                "type": "task_start",
                "task": func.__name__,
                "timestamp": start_time.isoformat(),
                "args": str(args) if args else None,
                "kwargs": {k: v for k, v in kwargs.items() if isinstance(v, (str, int, float, bool, list, dict))}
            })
            
            try:
                # Execute the function
                if inspect.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                
                # Record successful completion
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                manager.update_agent_status(agent_id, {
                    "status": "idle",
                    "last_task": func.__name__,
                    "last_task_duration": duration,
                    "last_task_completed_at": end_time.isoformat()
                })
                
                manager.record_interaction({
                    "agent_id": agent_id,
                    "type": "task_complete",
                    "task": func.__name__,
                    "timestamp": end_time.isoformat(),
                    "duration": duration,
                    "success": True
                })
                
                return result
                
            except Exception as e:
                # Record error
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                manager.update_agent_status(agent_id, {
                    "status": "error",
                    "last_error": str(e),
                    "last_task": func.__name__,
                    "last_task_duration": duration,
                    "last_task_completed_at": end_time.isoformat()
                })
                
                manager.record_interaction({
                    "agent_id": agent_id,
                    "type": "task_error",
                    "task": func.__name__,
                    "timestamp": end_time.isoformat(),
                    "duration": duration,
                    "error": str(e),
                    "success": False
                })
                
                # Re-raise the exception
                raise
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Record start of activity
            start_time = datetime.now()
            
            # Update agent status to "busy"
            manager.update_agent_status(agent_id, {
                "status": "busy",
                "current_task": func.__name__,
                "started_at": start_time.isoformat()
            })
            
            # Record interaction start
            interaction_id = manager.record_interaction({
                "agent_id": agent_id,
                "type": "task_start",
                "task": func.__name__,
                "timestamp": start_time.isoformat(),
                "args": str(args) if args else None,
                "kwargs": {k: v for k, v in kwargs.items() if isinstance(v, (str, int, float, bool, list, dict))}
            })
            
            try:
                # Execute the function
                result = func(*args, **kwargs)
                
                # Record successful completion
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                manager.update_agent_status(agent_id, {
                    "status": "idle",
                    "last_task": func.__name__,
                    "last_task_duration": duration,
                    "last_task_completed_at": end_time.isoformat()
                })
                
                manager.record_interaction({
                    "agent_id": agent_id,
                    "type": "task_complete",
                    "task": func.__name__,
                    "timestamp": end_time.isoformat(),
                    "duration": duration,
                    "success": True
                })
                
                return result
                
            except Exception as e:
                # Record error
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                manager.update_agent_status(agent_id, {
                    "status": "error",
                    "last_error": str(e),
                    "last_task": func.__name__,
                    "last_task_duration": duration,
                    "last_task_completed_at": end_time.isoformat()
                })
                
                manager.record_interaction({
                    "agent_id": agent_id,
                    "type": "task_error",
                    "task": func.__name__,
                    "timestamp": end_time.isoformat(),
                    "duration": duration,
                    "error": str(e),
                    "success": False
                })
                
                # Re-raise the exception
                raise
        
        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator

def register_agent(agent_id: str, metadata: Dict[str, Any]):
    """
    Register an agent with the WebSocket manager
    
    Args:
        agent_id: The ID of the agent
        metadata: Agent metadata (name, description, etc.)
    """
    manager.update_agent_status(agent_id, {
        "status": "idle",
        "registered_at": datetime.now().isoformat(),
        "metadata": metadata
    })
    
    logger.info(f"Agent registered: {agent_id}")
    
    # Record registration interaction
    manager.record_interaction({
        "agent_id": agent_id,
        "type": "agent_registered",
        "timestamp": datetime.now().isoformat(),
        "metadata": metadata
    }) 