"""
Model and Ollama utilities
"""

import ollama
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

def check_ollama_connection() -> bool:
    """
    Check if Ollama is running and accessible
    
    Returns:
        True if Ollama is accessible, False otherwise
    """
    try:
        ollama.list()
        return True
    except Exception as e:
        logger.error(f"Ollama connection failed: {e}")
        return False

def list_available_models() -> List[Dict[str, Any]]:
    """
    List all available models in Ollama
    
    Returns:
        List of model information dictionaries
    """
    try:
        response = ollama.list()
        return response.get("models", [])
    except Exception as e:
        logger.error(f"Failed to list models: {e}")
        return []

def get_model_info(model_name: str) -> Optional[Dict[str, Any]]:
    """
    Get information about a specific model
    
    Args:
        model_name: Name of the model
        
    Returns:
        Model information dictionary or None if not found
    """
    models = list_available_models()
    for model in models:
        if model.get("name") == model_name:
            return model
    return None

def check_model_availability(model_name: str) -> bool:
    """
    Check if a specific model is available
    
    Args:
        model_name: Name of the model to check
        
    Returns:
        True if model is available, False otherwise
    """
    return get_model_info(model_name) is not None

def format_model_size(size_bytes: int) -> str:
    """
    Format model size in human readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB" 