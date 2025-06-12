"""
Collaborative team of specialized agents
"""

from agno.team import Team
from agents import general_agent, search_agent, finance_agent, code_agent, system_agent
from agents.settings import get_model

collaborative_team = Team(
    name="CollaborativeTeam",
    mode="coordinate",
    model=get_model(),
    members=[general_agent, search_agent, finance_agent, code_agent, system_agent],
    instructions=[
        "Vous êtes une équipe d'experts spécialisés travaillant ensemble.",
        "Collaborez efficacement pour résoudre des problèmes complexes.",
        "Chaque agent utilise ses compétences spécialisées au bon moment.",
        "Partagez les informations pertinentes entre vous.",
        "Coordonnez vos efforts pour fournir une réponse complète.",
        "Évitez les redondances et maximisez la complémentarité."
    ],
    show_tool_calls=True,
    markdown=True,
    description="Équipe collaborative d'experts spécialisés"
) 