"""
Agent settings and configuration
"""

from agno.models.ollama import Ollama

# Default model configuration
DEFAULT_MODEL = "mistral:latest"
TEMPERATURE = 0.1

# Available models on the system
AVAILABLE_MODELS = [
    "mistral:latest",
    "llama3.2:3b",
    "llama3.2:latest", 
    "phi3:mini",
    "my-phi3:latest"
]

def get_model(model_name: str = DEFAULT_MODEL) -> Ollama:
    """Get an Ollama model instance"""
    return Ollama(id=model_name) 