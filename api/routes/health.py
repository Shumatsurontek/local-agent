"""
Health check routes
"""

from fastapi import APIRouter
from datetime import datetime
import ollama

router = APIRouter()

@router.get("/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Multi-Agent System API"
    }

@router.get("/ollama")
async def ollama_health():
    """Check Ollama connection"""
    try:
        # Try to list models to check if Ollama is running
        models = ollama.list()
        return {
            "status": "healthy",
            "ollama_connected": True,
            "models_count": len(models.get("models", [])),
            "available_models": [model["name"] for model in models.get("models", [])]
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "ollama_connected": False,
            "error": str(e)
        } 