"""
General purpose agent for conversation and basic tasks
"""

from agno.agent import Agent
from .settings import get_model

general_agent = Agent(
    name="GeneralAgent",
    model=get_model("qwen3:8b"),
    instructions=[
        "Tu es un assistant général intelligent et serviable.",
        "Réponds aux questions de culture générale avec précision.",
        "Fournis des explications claires et pédagogiques.",
        "Si tu as besoin d'outils spécialisés, recommande l'agent approprié.",
        "Sois concis mais complet dans tes réponses."
    ],
    markdown=True,
    show_tool_calls=True,
    description="Assistant général pour les conversations et tâches basiques"
) 