#!/usr/bin/env python3
"""
Test rapide d'un agent spécifique
"""

import sys
from rich.console import Console
from rich.panel import Panel

from main import AgentManager

console = Console()

def test_agent(agent_type: str, question: str):
    """Test rapide d'un agent"""
    try:
        console.print(f"[blue]🧪 Test de l'agent '{agent_type}'[/blue]")
        console.print(f"[dim]Question: {question}[/dim]\n")
        
        manager = AgentManager()
        
        if agent_type == "team":
            agent = manager.team
        else:
            agent = manager.get_agent(agent_type)
        
        if not agent:
            console.print(f"[red]❌ Agent '{agent_type}' non trouvé[/red]")
            return
        
        response = agent.run(question)
        
        console.print(Panel(
            response.content,
            title=f"[bold green]🤖 {agent.name}[/bold green]",
            border_style="green"
        ))
        
    except Exception as e:
        console.print(f"[red]❌ Erreur: {e}[/red]")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        console.print("[red]Usage: python quick_test.py <agent_type> <question>[/red]")
        console.print("[dim]Exemple: python quick_test.py general 'Bonjour'[/dim]")
        sys.exit(1)
    
    agent_type = sys.argv[1]
    question = sys.argv[2]
    
    test_agent(agent_type, question) 