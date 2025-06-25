"""
Programming and computation agent using Python tools
"""

from agno.agent import Agent
from agno.tools.python import PythonTools
from .settings import get_model

code_agent = Agent(
    name="CodeAgent",
    model=get_model("qwen2.5-coder:7b"),
    tools=[PythonTools()],
    instructions=[
        "Tu es un expert en programmation qui DOIT utiliser Python pour résoudre les problèmes.",
        "RÈGLE ABSOLUE: Pour toute demande de code ou calcul, tu DOIS utiliser les outils Python.",
        "Processus obligatoire:",
        "1. Analyse le problème demandé",
        "2. Écris et exécute le code Python avec les outils disponibles",
        "3. Montre les résultats de l'exécution",
        "4. Explique la solution avec le code exécuté",
        "Ne réponds JAMAIS avec du code théorique - exécute toujours le code avec tes outils.",
        "Exemple: Pour 'fonction fibonacci', écris et exécute le code Python."
    ],
    markdown=True,
    reasoning=False,
    show_tool_calls=True,
    description="Expert en programmation et calculs"
) 