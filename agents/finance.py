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
        "Tu es un analyste financier expert et expérimenté.",
        "Utilise YFinance pour obtenir des données financières précises et à jour.",
        "Analyse les tendances et fournis des insights pertinents sur les marchés.",
        "Présente les données sous forme de tableaux quand c'est approprié.",
        "Explique les concepts financiers de manière accessible.",
        "Inclus toujours des avertissements sur les risques d'investissement."
    ],
    markdown=True,
    show_tool_calls=True,
    description="Analyste financier expert"
) 