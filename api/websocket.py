"""
WebSocket manager for real-time agent updates
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Any, Optional
import json
import asyncio
import logging
from datetime import datetime
from uuid import uuid4

logger = logging.getLogger(__name__)

class ConnectionManager:
    """WebSocket connection manager for real-time updates"""
    
    def __init__(self):
        # Active connections
        self.active_connections: Dict[str, WebSocket] = {}
        # Agent status
        self.agent_status: Dict[str, Dict[str, Any]] = {}
        # Agent interactions
        self.interactions: List[Dict[str, Any]] = []
        # Background task
        self.background_task: Optional[asyncio.Task] = None
    
    async def connect(self, websocket: WebSocket) -> str:
        """Connect a client and return connection ID"""
        await websocket.accept()
        connection_id = str(uuid4())
        self.active_connections[connection_id] = websocket
        logger.info(f"Client connected: {connection_id}")
        
        # Send initial state
        await self.send_initial_state(connection_id)
        
        # Start background task if not running
        if self.background_task is None or self.background_task.done():
            self.background_task = asyncio.create_task(self.send_periodic_updates())
            
        return connection_id
    
    def disconnect(self, connection_id: str):
        """Disconnect a client"""
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
            logger.info(f"Client disconnected: {connection_id}")
    
    async def send_personal_message(self, message: Dict[str, Any], connection_id: str):
        """Send a message to a specific client"""
        if connection_id in self.active_connections:
            await self.active_connections[connection_id].send_json(message)
    
    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast a message to all connected clients"""
        disconnected = []
        for connection_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message)
            except RuntimeError:
                disconnected.append(connection_id)
        
        # Clean up disconnected clients
        for connection_id in disconnected:
            self.disconnect(connection_id)
    
    async def send_initial_state(self, connection_id: str):
        """Send initial state to a new client"""
        await self.send_personal_message({
            "type": "initial_state",
            "data": {
                "agents": self.agent_status,
                "interactions": self.interactions[-50:] if self.interactions else []
            }
        }, connection_id)
    
    async def send_periodic_updates(self):
        """Send periodic updates to all clients"""
        while True:
            try:
                await self.broadcast({
                    "type": "heartbeat",
                    "timestamp": datetime.now().isoformat()
                })
                await asyncio.sleep(30)  # Send heartbeat every 30 seconds
            except Exception as e:
                logger.error(f"Error in periodic updates: {e}")
                await asyncio.sleep(5)
    
    def update_agent_status(self, agent_id: str, status: Dict[str, Any]):
        """Update agent status and broadcast to clients"""
        self.agent_status[agent_id] = {
            **status,
            "last_updated": datetime.now().isoformat()
        }
        
        # Create task to broadcast the update only if event loop is running
        try:
            asyncio.create_task(self.broadcast({
                "type": "agent_update",
                "agent_id": agent_id,
                "data": self.agent_status[agent_id]
            }))
        except RuntimeError:
            # No event loop running, skip broadcast
            logger.debug(f"No event loop running, skipping broadcast for agent {agent_id}")
    
    def record_interaction(self, interaction: Dict[str, Any]) -> str:
        """Record an agent interaction and broadcast to clients"""
        # Add timestamp if not present
        if "timestamp" not in interaction:
            interaction["timestamp"] = datetime.now().isoformat()
            
        # Add unique ID
        interaction_id = str(uuid4())
        interaction["id"] = interaction_id
        
        # Add to interactions list
        self.interactions.append(interaction)
        
        # Keep only last 1000 interactions
        if len(self.interactions) > 1000:
            self.interactions = self.interactions[-1000:]
        
        # Broadcast the interaction only if event loop is running
        try:
            asyncio.create_task(self.broadcast({
                "type": "new_interaction",
                "data": interaction
            }))
        except RuntimeError:
            # No event loop running, skip broadcast
            logger.debug("No event loop running, skipping interaction broadcast")
        
        return interaction_id

# Global connection manager instance
manager = ConnectionManager() 