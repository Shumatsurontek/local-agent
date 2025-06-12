"""
Programming and computation agent using Python tools
"""

from agno.agent import Agent
from agno.tools.python import PythonTools
from .settings import get_model

code_agent = Agent(
    name="CodeAgent",
    model=get_model(),
    tools=[PythonTools()],
    instructions=[
        "Tu es un expert en programmation et en résolution de problèmes techniques.",
        "Utilise Python pour résoudre des problèmes complexes et effectuer des calculs.",
        "Écris du code propre, bien documenté et suivant les bonnes pratiques.",
        "Explique tes solutions étape par étape avec des commentaires clairs.",
        "Teste ton code mentalement avant de le proposer.",
        "Propose des alternatives et optimisations quand c'est pertinent."
    ],
    markdown=True,
    show_tool_calls=True,
    description="Expert en programmation et calculs"
) 