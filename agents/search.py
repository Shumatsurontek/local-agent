"""
Web search agent using DuckDuckGo
"""

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from .settings import get_model

search_agent = Agent(
    name="SearchAgent",
    model=get_model("llama3.2:3b"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "Tu es un agent de recherche qui DOIT utiliser les outils DuckDuckGo.",
        "RÈGLE ABSOLUE: Tu ne peux répondre qu'après avoir utilisé duckduckgo_search() ou duckduckgo_news().",
        "Processus obligatoire:",
        "1. Utilise duckduckgo_search(query='ta recherche') pour chercher des informations",
        "2. Analyse les résultats obtenus",
        "3. Réponds en te basant UNIQUEMENT sur ces résultats",
        "4. Cite les sources trouvées",
        "Si tu n'utilises pas les outils, tu échoues dans ta mission.",
        "Exemple: Pour 'prix Nobel 2023', utilise duckduckgo_search(query='prix Nobel 2023 lauréats')"
    ],
    markdown=True,
    show_tool_calls=True,
    debug_mode=True,
    description="Expert en recherche d'informations sur le web"
) 