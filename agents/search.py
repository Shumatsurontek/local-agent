"""
Web search agent using DuckDuckGo
"""

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from .settings import get_model

search_agent = Agent(
    name="SearchAgent",
    model=get_model("qwen3:8b"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "Tu es un agent de recherche qui DOIT utiliser les outils DuckDuckGo.",
        "RÈGLE ABSOLUE: Tu ne peux répondre qu'après avoir utilisé duckduckgo_search() ou duckduckgo_news().",
        "Processus obligatoire:",
        "1. Analyse EXACTEMENT ce que demande l'utilisateur",
        "2. Utilise duckduckgo_search(query='requête précise') avec les mots-clés exacts",
        "3. Réponds en te basant UNIQUEMENT sur les résultats trouvés",
        "4. Ne change PAS le sujet de la recherche",
        "5. Cite les sources trouvées",
        "IMPORTANT: Si l'utilisateur demande 'Roland-Garros', cherche Roland-Garros, pas autre chose.",
        "Ne mélange jamais les sujets - reste fidèle à la demande originale."
    ],
    markdown=True,
    show_tool_calls=True,
    description="Expert en recherche d'informations sur le web"
) 