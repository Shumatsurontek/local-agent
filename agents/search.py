"""
Web search agent using DuckDuckGo
"""

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from .settings import get_model

search_agent = Agent(
    name="SearchAgent",
    model=get_model(),
    tools=[DuckDuckGoTools()],
    instructions=[
        "Tu es un expert en recherche d'informations sur le web.",
        "Utilise DuckDuckGo pour trouver des informations précises et récentes.",
        "Fournis des réponses détaillées avec des sources quand possible.",
        "Résume les informations importantes de manière claire et structurée.",
        "Vérifie la crédibilité des sources trouvées."
    ],
    markdown=True,
    show_tool_calls=True,
    description="Expert en recherche d'informations sur le web"
) 