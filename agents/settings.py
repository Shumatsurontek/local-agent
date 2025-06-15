"""
Agent settings and configuration
"""

import os
from agno.models.ollama import Ollama
import logging

# Configure Ollama logging
ollama_logger = logging.getLogger('ollama')

def get_model(model_name: str = "mistral:latest") -> Ollama:
    """Get configured Ollama model with logging"""
    ollama_logger.info(f"🔧 Creating Ollama model: {model_name}")
    
    model = Ollama(
        id=model_name,
        host=os.getenv("OLLAMA_HOST", "http://localhost:11434")
    )
    
    ollama_logger.debug(f"🔧 Model config - Host: {model.host}")
    ollama_logger.debug(f"🔧 Model config - ID: {model.id}")
    
    return model

# Default model configuration
DEFAULT_MODEL = get_model()

# Model configurations for each agent type
AGENT_MODELS = {
    "general": "qwen3:8b",
    "search": "qwen3:8b", 
    "finance": "qwen3:8b",
    "code": "qwen2.5-coder:7b",
    "system": "phi3:mini"
}

# Available models on the system
AVAILABLE_MODELS = [
    "mistral:latest",
    "llama3.2:3b",
    "llama3.2:latest", 
    "phi3:mini",
    "my-phi3:latest",
    "qwen2.5-coder:7b",
    "deepseek-r1:8b",
    "qwen3:8b"
] 