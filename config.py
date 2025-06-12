"""
Configuration centralisée pour le Multi-Agent System
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path

@dataclass
class ModelConfig:
    """Configuration des modèles Ollama"""
    default_model: str = "mistral:latest"
    available_models: List[str] = None
    temperature: float = 0.1
    max_tokens: Optional[int] = None
    
    def __post_init__(self):
        if self.available_models is None:
            self.available_models = [
                "mistral:latest",
                "llama3.2:3b",
                "llama3.2:latest", 
                "phi3:mini",
                "my-phi3:latest"
            ]

@dataclass
class AgentConfig:
    """Configuration d'un agent spécifique"""
    name: str
    description: str
    instructions: List[str]
    tools: List[str]
    emoji: str
    specialized_model: Optional[str] = None

class AgentsConfig:
    """Configuration de tous les agents"""
    
    AGENTS: Dict[str, AgentConfig] = {
        "general": AgentConfig(
            name="GeneralAgent",
            description="Assistant général intelligent",
            emoji="🤖",
            instructions=[
                "Tu es un assistant général intelligent et serviable.",
                "Réponds aux questions de culture générale avec précision.",
                "Fournis des explications claires et pédagogiques.",
                "Si tu as besoin d'outils spécialisés, recommande l'agent approprié.",
                "Sois concis mais complet dans tes réponses."
            ],
            tools=[]
        ),
        
        "search": AgentConfig(
            name="SearchAgent", 
            description="Expert en recherche d'informations sur le web",
            emoji="🔍",
            instructions=[
                "Tu es un expert en recherche d'informations sur le web.",
                "Utilise DuckDuckGo pour trouver des informations précises et récentes.",
                "Fournis des réponses détaillées avec des sources quand possible.",
                "Résume les informations importantes de manière claire et structurée.",
                "Vérifie la crédibilité des sources trouvées."
            ],
            tools=["duckduckgo"]
        ),
        
        "finance": AgentConfig(
            name="FinanceAgent",
            description="Analyste financier expert", 
            emoji="💰",
            instructions=[
                "Tu es un analyste financier expert et expérimenté.",
                "Utilise YFinance pour obtenir des données financières précises et à jour.",
                "Analyse les tendances et fournis des insights pertinents sur les marchés.",
                "Présente les données sous forme de tableaux quand c'est approprié.",
                "Explique les concepts financiers de manière accessible.",
                "Inclus toujours des avertissements sur les risques d'investissement."
            ],
            tools=["yfinance"]
        ),
        
        "code": AgentConfig(
            name="CodeAgent",
            description="Expert en programmation et calculs",
            emoji="💻", 
            instructions=[
                "Tu es un expert en programmation et en résolution de problèmes techniques.",
                "Utilise Python pour résoudre des problèmes complexes et effectuer des calculs.",
                "Écris du code propre, bien documenté et suivant les bonnes pratiques.",
                "Explique tes solutions étape par étape avec des commentaires clairs.",
                "Teste ton code mentalement avant de le proposer.",
                "Propose des alternatives et optimisations quand c'est pertinent."
            ],
                         tools=["python"],
             specialized_model="mistral:latest"
        ),
        
        "system": AgentConfig(
            name="SystemAgent",
            description="Administrateur système expert",
            emoji="⚙️",
            instructions=[
                "Tu es un administrateur système expert et prudent.",
                "Utilise les commandes shell pour des tâches système appropriées.",
                "TOUJOURS expliquer ce que font les commandes avant de les exécuter.",
                "Sois extrêmement prudent avec les commandes destructives.",
                "Propose des alternatives sûres quand possible.",
                "Vérifie les permissions et la sécurité avant d'agir."
            ],
            tools=["shell"]
        )
    }
    
    TEAM_CONFIG = {
        "name": "AgentTeam",
        "description": "Équipe collaborative d'experts spécialisés",
        "emoji": "👥",
        "instructions": [
            "Vous êtes une équipe d'experts spécialisés travaillant ensemble.",
            "Collaborez efficacement pour résoudre des problèmes complexes.",
            "Chaque agent utilise ses compétences spécialisées au bon moment.",
            "Partagez les informations pertinentes entre vous.",
            "Coordonnez vos efforts pour fournir une réponse complète.",
            "Évitez les redondances et maximisez la complémentarité."
        ]
    }

@dataclass 
class AppConfig:
    """Configuration générale de l'application"""
    app_name: str = "Multi-Agent System avec Agno"
    version: str = "1.0.0"
    author: str = "Local Agent Team"
    
    # Chemins
    base_dir: Path = Path(__file__).parent
    logs_dir: Path = base_dir / "logs"
    data_dir: Path = base_dir / "data"
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Interface
    max_response_length: int = 2000  # Pour l'affichage tronqué
    show_tool_calls: bool = True
    markdown_output: bool = True
    
    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_timeout: int = 300  # 5 minutes
    
    def __post_init__(self):
        # Créer les dossiers nécessaires
        self.logs_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)

# Instances globales
MODEL_CONFIG = ModelConfig()
AGENTS_CONFIG = AgentsConfig()
APP_CONFIG = AppConfig()

# Utilitaires
def get_agent_config(agent_id: str) -> Optional[AgentConfig]:
    """Récupère la configuration d'un agent"""
    return AGENTS_CONFIG.AGENTS.get(agent_id)

def list_available_agents() -> Dict[str, str]:
    """Liste les agents disponibles avec leurs descriptions"""
    agents = {
        agent_id: f"{config.emoji} {config.description}"
        for agent_id, config in AGENTS_CONFIG.AGENTS.items()
    }
    agents["team"] = f"{AGENTS_CONFIG.TEAM_CONFIG['emoji']} {AGENTS_CONFIG.TEAM_CONFIG['description']}"
    return agents

def get_model_for_agent(agent_id: str) -> str:
    """Récupère le modèle recommandé pour un agent"""
    config = get_agent_config(agent_id)
    if config and config.specialized_model:
        return config.specialized_model
    return MODEL_CONFIG.default_model 