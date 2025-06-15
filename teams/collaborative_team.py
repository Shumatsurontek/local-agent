"""
Collaborative team of specialized agents
"""

from agno.team import Team
from agno.models.ollama import Ollama
from agents import search_agent, finance_agent, code_agent, system_agent
from agents.settings import get_model

# Utiliser un modèle plus puissant pour le team leader
# Essayer llama3.2:latest en alternative
powerful_model = Ollama(id="llama3.2:latest", host="http://localhost:11434")

collaborative_team = Team(
    name="CollaborativeTeam",
    mode="coordinate",  # Mode coordinate pour délégation intelligente
    model=powerful_model,  # Modèle plus puissant pour le leader
    members=[search_agent, finance_agent, code_agent, system_agent],  # Agents spécialisés uniquement
    instructions=[
        "Tu es le coordinateur d'une équipe d'experts. Ton rôle est d'EXÉCUTER les tâches.",
        "PROCESS: Pour chaque demande, tu DOIS:",
        "1. Identifier immédiatement les agents appropriés",
        "2. Utiliser transfer_task_to_member pour déléguer",
        "3. Attendre que TOUS les agents terminent leurs tâches",
        "4. Consolider leurs réponses en UNE réponse finale",
        "RÈGLE ABSOLUE: Ne jamais montrer de plan ou d'étapes - EXÉCUTE directement.",
        "Donne seulement la réponse finale avec les vraies données."
    ],
    show_tool_calls=True,  # Affiche les délégations aux agents (pour voir l'orchestration)
    show_members_responses=True,  # Affiche les réponses des membres
    enable_agentic_context=True,  # Active le contexte agentique
    markdown=True,
    success_criteria="L'équipe a fourni une réponse finale avec les données réelles consolidées.",
    description="Équipe collaborative avec coordinateur puissant (Llama3.2) et agents spécialisés"
)

# Version complète avec recherche (plus lente à cause des rate limits)
# from agents import search_agent
# collaborative_team_full = Team(
#     name="CollaborativeTeamFull", 
#     mode="coordinate",
#     model=get_model(),
#     members=[general_agent, search_agent, finance_agent, code_agent, system_agent],
#     instructions=[
#         "Vous êtes une équipe d'experts spécialisés travaillant ensemble.",
#         "Collaborez efficacement pour résoudre des problèmes complexes.",
#         "Chaque agent utilise ses compétences spécialisées au bon moment.",
#         "Partagez les informations pertinentes entre vous.",
#         "Coordonnez vos efforts pour fournir une réponse complète.",
#         "Évitez les redondances et maximisez la complémentarité."
#     ],
#     show_tool_calls=True,
#     markdown=True,
#     description="Équipe collaborative d'experts spécialisés (version complète)"
# ) 