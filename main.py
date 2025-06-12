#!/usr/bin/env python3
"""
Multi-Agent System using Agno framework with Ollama
Différents agents spécialisés pour diverses tâches
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from typing import Optional
import asyncio
import logging

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.python import PythonTools
from agno.tools.shell import ShellTools
from agno.team import Team

from config import (
    MODEL_CONFIG, AGENTS_CONFIG, APP_CONFIG,
    get_agent_config, list_available_agents, get_model_for_agent
)

# Configuration
console = Console()
app = typer.Typer(help="🤖 Multi-Agent System avec Agno")

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentManager:
    """Gestionnaire des agents spécialisés"""
    
    def __init__(self, model_name: str = "mistral"):
        self.model = Ollama(id=model_name)
        self.agents = self._create_agents()
        self.team = self._create_team()
    
    def _create_agents(self) -> dict[str, Agent]:
        """Crée les différents agents spécialisés à partir de la configuration"""
        agents = {}
        
        # Mapping des outils
        tool_mapping = {
            "duckduckgo": DuckDuckGoTools(),
            "yfinance": YFinanceTools(
                stock_price=True,
                analyst_recommendations=True,
                company_info=True,
                company_news=True
            ),
            "python": PythonTools(),
            "shell": ShellTools()
        }
        
        # Créer chaque agent à partir de sa configuration
        for agent_id, config in AGENTS_CONFIG.AGENTS.items():
            # Sélectionner le modèle approprié
            model = self.model
            if config.specialized_model and config.specialized_model != self.model.id:
                model = Ollama(id=config.specialized_model)
            
            # Sélectionner les outils
            tools = [tool_mapping[tool_name] for tool_name in config.tools if tool_name in tool_mapping]
            
            # Créer l'agent
            agent = Agent(
                name=config.name,
                model=model,
                tools=tools,
                instructions=config.instructions,
                markdown=APP_CONFIG.markdown_output,
                show_tool_calls=APP_CONFIG.show_tool_calls
            )
            
            agents[agent_id] = agent
        
        return agents
    
    def _create_team(self) -> Team:
        """Crée une équipe d'agents collaboratifs"""
        return Team(
            name=AGENTS_CONFIG.TEAM_CONFIG["name"],
            mode="coordinate",
            model=self.model,
            members=list(self.agents.values()),
            instructions=AGENTS_CONFIG.TEAM_CONFIG["instructions"],
            show_tool_calls=APP_CONFIG.show_tool_calls,
            markdown=APP_CONFIG.markdown_output
        )
    
    def get_agent(self, agent_type: str) -> Optional[Agent]:
        """Récupère un agent spécifique"""
        return self.agents.get(agent_type)
    
    def list_agents(self) -> dict[str, str]:
        """Liste les agents disponibles avec leurs descriptions"""
        return list_available_agents()

def display_welcome():
    """Affiche le message de bienvenue"""
    console.print(Panel.fit(
        f"[bold blue]{APP_CONFIG.app_name}[/bold blue]\n"
        f"[dim]Version {APP_CONFIG.version} - Powered by Ollama[/dim]",
        border_style="blue"
    ))

def display_agents(manager: AgentManager):
    """Affiche la liste des agents disponibles"""
    table = Table(title="Agents Disponibles", show_header=True)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    
    for agent_id, description in manager.list_agents().items():
        table.add_row(agent_id, description)
    
    console.print(table)

@app.command()
def chat(
    agent: str = typer.Option("general", help="Type d'agent à utiliser"),
    model: str = typer.Option("mistral", help="Modèle Ollama à utiliser")
):
    """Lance une session de chat avec un agent spécifique"""
    
    display_welcome()
    
    try:
        manager = AgentManager(model_name=model)
        
        if agent not in manager.list_agents():
            console.print(f"[red]❌ Agent '{agent}' non trouvé[/red]")
            display_agents(manager)
            return
        
        console.print(f"[green]✅ Agent '{agent}' initialisé avec le modèle '{model}'[/green]")
        console.print("[dim]Tapez 'quit' pour quitter, 'agents' pour voir la liste[/dim]\n")
        
        while True:
            try:
                question = Prompt.ask("\n[bold cyan]💬 Votre question[/bold cyan]")
                
                if question.lower() in ['quit', 'exit', 'q']:
                    console.print("[yellow]👋 Au revoir![/yellow]")
                    break
                
                if question.lower() == 'agents':
                    display_agents(manager)
                    continue
                
                if not question.strip():
                    continue
                
                # Sélectionner l'agent ou l'équipe
                if agent == "team":
                    selected_agent = manager.team
                else:
                    selected_agent = manager.get_agent(agent)
                
                if not selected_agent:
                    console.print(f"[red]❌ Erreur: agent '{agent}' non disponible[/red]")
                    continue
                
                console.print(f"[dim]🔄 {selected_agent.name} traite votre demande...[/dim]")
                
                # Exécuter la requête
                response = selected_agent.run(question)
                
                # Afficher la réponse
                console.print(Panel(
                    response.content,
                    title=f"[bold green]🤖 {selected_agent.name}[/bold green]",
                    border_style="green"
                ))
                
            except KeyboardInterrupt:
                console.print("\n[yellow]👋 Au revoir![/yellow]")
                break
            except Exception as e:
                console.print(f"[red]❌ Erreur: {e}[/red]")
                logger.error(f"Erreur lors du chat: {e}")
    
    except Exception as e:
        console.print(f"[red]❌ Erreur d'initialisation: {e}[/red]")
        logger.error(f"Erreur d'initialisation: {e}")

@app.command()
def list_agents(
    model: str = typer.Option("mistral", help="Modèle Ollama à utiliser")
):
    """Liste tous les agents disponibles"""
    
    display_welcome()
    
    try:
        manager = AgentManager(model_name=model)
        display_agents(manager)
        
        console.print(f"\n[dim]Utilisez: python main.py chat --agent <ID> --model {model}[/dim]")
        
    except Exception as e:
        console.print(f"[red]❌ Erreur: {e}[/red]")

@app.command()
def demo():
    """Démonstration rapide avec différents agents"""
    
    display_welcome()
    console.print("[bold yellow]🎯 Démonstration des agents[/bold yellow]\n")
    
    try:
        manager = AgentManager()
        
        demos = [
            ("general", "Explique-moi ce qu'est l'intelligence artificielle en 3 phrases"),
            ("code", "Calcule la factorielle de 5 et montre le code Python"),
            ("search", "Trouve les dernières nouvelles sur l'IA"),
        ]
        
        for agent_type, question in demos:
            console.print(f"[bold cyan]🔸 Test de l'agent '{agent_type}'[/bold cyan]")
            console.print(f"[dim]Question: {question}[/dim]")
            
            agent = manager.get_agent(agent_type)
            if agent:
                try:
                    response = agent.run(question)
                    console.print(Panel(
                        response.content[:300] + "..." if len(response.content) > 300 else response.content,
                        title=f"[green]{agent.name}[/green]",
                        border_style="green"
                    ))
                except Exception as e:
                    console.print(f"[red]❌ Erreur avec {agent_type}: {e}[/red]")
            
            console.print()
    
    except Exception as e:
        console.print(f"[red]❌ Erreur de démonstration: {e}[/red]")

if __name__ == "__main__":
    app()


