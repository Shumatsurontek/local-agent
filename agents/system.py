"""
System administration agent using shell tools
"""

from agno.agent import Agent
from agno.tools.shell import ShellTools
from .settings import get_model

system_agent = Agent(
    name="SystemAgent",
    model=get_model(),
    tools=[ShellTools()],
    instructions=[
        "Tu es un administrateur système expert et prudent.",
        "Utilise les commandes shell pour des tâches système appropriées.",
        "TOUJOURS expliquer ce que font les commandes avant de les exécuter.",
        "Sois extrêmement prudent avec les commandes destructives.",
        "Propose des alternatives sûres quand possible.",
        "Vérifie les permissions et la sécurité avant d'agir."
    ],
    markdown=True,
    reasoning=False,
    show_tool_calls=True,
    description="Administrateur système expert"
) 