"""
Main FastAPI application
"""

import logging
import sys
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import agents, teams, health, websocket
from api.settings import API_SETTINGS

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('ollama_backend.log')
    ]
)

# Create specific loggers
ollama_logger = logging.getLogger('ollama')
agent_logger = logging.getLogger('agents')
api_logger = logging.getLogger('api')

# Set log levels
ollama_logger.setLevel(logging.DEBUG)
agent_logger.setLevel(logging.DEBUG)
api_logger.setLevel(logging.INFO)

# Create FastAPI app
app = FastAPI(
    title=API_SETTINGS.title,
    description=API_SETTINGS.description,
    version=API_SETTINGS.version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = datetime.now()
    api_logger.info(f"🔵 REQUEST: {request.method} {request.url}")
    
    response = await call_next(request)
    
    process_time = (datetime.now() - start_time).total_seconds()
    api_logger.info(f"🟢 RESPONSE: {response.status_code} - {process_time:.3f}s")
    
    return response

# Include routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(agents.router, prefix="/agents", tags=["Agents"])
app.include_router(teams.router, prefix="/teams", tags=["Teams"])
app.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Multi-Agent System API",
        "version": API_SETTINGS.version,
        "docs": "/docs",
        "websocket": "/ws"
    } 