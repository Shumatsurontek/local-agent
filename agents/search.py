"""
Web search agent using Tavily
"""

from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from .settings import get_model

search_agent = Agent(
    name="SearchAgent",
    model=get_model("qwen3:8b"),
    tools=[TavilyTools()],
    instructions=[
        "Tu es un agent de recherche spécialisé dans la recherche d'informations actuelles.",
        "Tu utilises Tavily pour obtenir des informations récentes et fiables.",
        "Processus recommandé:",
        "1. Analyse précisément ce que demande l'utilisateur",
        "2. Utilise tavily_search() avec les mots-clés appropriés en anglais ou français",
        "3. Fournis des informations basées sur les résultats trouvés",
        "4. Cite les sources trouvées avec leurs URLs",
        "5. Si la recherche échoue, explique la situation et fournis ce que tu peux",
        "IMPORTANT: Reste fidèle à la demande originale et fournis des informations récentes."
    ],
    markdown=True,
    reasoning=False,
    show_tool_calls=True,
    description="Expert en recherche d'informations sur le web avec Tavily"
) 