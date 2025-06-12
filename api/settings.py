"""
API settings and configuration
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class APISettings:
    """API configuration settings"""
    title: str = "Multi-Agent System API"
    description: str = "FastAPI application for serving Agno agents and teams with Ollama"
    version: str = "1.0.0"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    log_level: str = "info"
    
    # Ollama settings
    ollama_host: str = "http://localhost:11434"
    ollama_timeout: int = 300
    
    # CORS settings
    cors_origins: list[str] = None
    
    def __post_init__(self):
        if self.cors_origins is None:
            self.cors_origins = ["*"]

# Global settings instance
API_SETTINGS = APISettings() 