"""
Financial analysis agent using YFinance
"""

from agno.agent import Agent
from agno.tools.yfinance import YFinanceTools
from .settings import get_model

finance_agent = Agent(
    name="FinanceAgent",
    model=get_model(),
    tools=[YFinanceTools(
        stock_price=True,
        analyst_recommendations=True,
        company_info=True,
        company_news=True
    )],
    instructions=[
        "Tu es un analyste financier expert avec accès aux outils YFinance.",
        "Quand on te demande des informations financières, utilise TOUJOURS tes outils:",
        "- get_current_stock_price(symbol) pour obtenir le prix actuel d'une action",
        "- get_company_info(symbol) pour obtenir les informations d'une entreprise", 
        "- get_analyst_recommendations(symbol) pour les recommandations d'analystes",
        "- get_company_news(symbol) pour les actualités d'une entreprise",
        "Utilise tes outils pour obtenir des données réelles et à jour.",
        "Analyse les données obtenues et fournis des insights pertinents.",
        "Présente les résultats de manière claire et structurée."
    ],
    markdown=True,
    show_tool_calls=True,
    description="Analyste financier expert"
) 