"""
Agno workspace settings
"""

from dataclasses import dataclass

@dataclass
class WorkspaceSettings:
    """Workspace configuration settings"""
    # Application settings
    ws_name: str = "local-agent-agno"
    
    # Database settings
    db_app: str = "local_agent_db"
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_schema: str = "local_agent"
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Streamlit settings
    streamlit_host: str = "0.0.0.0"
    streamlit_port: int = 8501
    
    # Development settings
    dev_mode: bool = True
    debug_mode: bool = True
    
    # File paths
    data_dir: str = "data"
    logs_dir: str = "logs"
    
    # Ollama settings
    ollama_host: str = "http://localhost:11434"

# Workspace configuration instance
ws_settings = WorkspaceSettings() 