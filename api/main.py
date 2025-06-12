"""
Main FastAPI application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import agents, teams, health, websocket
from api.settings import API_SETTINGS

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