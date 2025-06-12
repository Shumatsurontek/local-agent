"""
WebSocket routes for real-time updates
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
import json
import logging
from api.websocket import manager
from typing import Dict, Any

logger = logging.getLogger(__name__)

router = APIRouter()

@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    connection_id = await manager.connect(websocket)
    try:
        while True:
            # Wait for messages from the client
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                # Process client messages
                if message.get("type") == "ping":
                    await manager.send_personal_message({"type": "pong"}, connection_id)
                elif message.get("type") == "subscribe":
                    # Client can subscribe to specific agents/teams
                    pass
            except json.JSONDecodeError:
                logger.warning(f"Received invalid JSON: {data}")
    except WebSocketDisconnect:
        manager.disconnect(connection_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(connection_id)

@router.get("/status")
async def websocket_status():
    """Get WebSocket connection status"""
    return {
        "active_connections": len(manager.active_connections),
        "agents_monitored": len(manager.agent_status),
        "interactions_recorded": len(manager.interactions)
    } 