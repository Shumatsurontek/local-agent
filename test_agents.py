#!/usr/bin/env python3
"""
Script de test rapide pour les agents
"""

import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from main import AgentManager
from config import APP_CONFIG, MODEL_CONFIG

console = Console()

async def test_agent_creation():
    """Test la création des agents"""
    console.print("[blue]🧪 Test de création des agents...[/blue]")
    
    try:
        manager = AgentManager()
        console.print(f"[green]✅ {len(manager.agents)} agents créés avec succès[/green]")
        
        # Lister les agents
        for agent_id, agent in manager.agents.items():
            console.print(f"  - {agent_id}: {agent.name}")
        
        return True
    except Exception as e:
        console.print(f"[red]❌ Erreur lors de la création: {e}[/red]")
        return False

async def test_simple_queries():
    """Test des requêtes simples"""
    console.print("[blue]🧪 Test de requêtes simples...[/blue]")
    
    try:
        manager = AgentManager()
        
        # Test de l'agent général
        general_agent = manager.get_agent("general")
        if general_agent:
            console.print("[dim]Test de l'agent général...[/dim]")
            response = general_agent.run("Bonjour, peux-tu te présenter en une phrase ?")
            console.print(f"[green]✅ Agent général répond: {response.content[:100]}...[/green]")
        
        return True
    except Exception as e:
        console.print(f"[red]❌ Erreur lors des tests: {e}[/red]")
        return False

async def test_configuration():
    """Test de la configuration"""
    console.print("[blue]🧪 Test de la configuration...[/blue]")
    
    try:
        # Vérifier la config
        console.print(f"  - App: {APP_CONFIG.app_name} v{APP_CONFIG.version}")
        console.print(f"  - Modèle par défaut: {MODEL_CONFIG.default_model}")
        console.print(f"  - Modèles disponibles: {len(MODEL_CONFIG.available_models)}")
        
        # Vérifier les dossiers
        if APP_CONFIG.logs_dir.exists():
            console.print(f"  - Dossier logs: ✅ {APP_CONFIG.logs_dir}")
        else:
            console.print(f"  - Dossier logs: ❌ {APP_CONFIG.logs_dir}")
        
        console.print("[green]✅ Configuration OK[/green]")
        return True
    except Exception as e:
        console.print(f"[red]❌ Erreur de configuration: {e}[/red]")
        return False

async def main():
    """Fonction principale de test"""
    console.print(Panel.fit(
        "[bold green]🧪 Tests du Multi-Agent System[/bold green]",
        border_style="green"
    ))
    
    tests = [
        ("Configuration", test_configuration),
        ("Création des agents", test_agent_creation),
        ("Requêtes simples", test_simple_queries),
    ]
    
    results = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        for test_name, test_func in tests:
            task = progress.add_task(f"Exécution: {test_name}", total=None)
            
            try:
                result = await test_func()
                results.append((test_name, result))
                progress.update(task, description=f"✅ {test_name}")
            except Exception as e:
                results.append((test_name, False))
                progress.update(task, description=f"❌ {test_name}: {e}")
            
            progress.remove_task(task)
    
    # Résumé
    console.print("\n" + "="*50)
    console.print("[bold blue]📊 Résumé des tests[/bold blue]")
    console.print("="*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        console.print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    console.print(f"\n[bold]Résultat: {passed}/{len(results)} tests réussis[/bold]")
    
    if passed == len(results):
        console.print("[bold green]🎉 Tous les tests sont passés ![/bold green]")
        console.print("\n[dim]Vous pouvez maintenant utiliser:[/dim]")
        console.print("[dim]python main.py list-agents[/dim]")
        console.print("[dim]python main.py chat --agent general[/dim]")
    else:
        console.print("[bold red]⚠️ Certains tests ont échoué[/bold red]")
        console.print("[dim]Vérifiez que Ollama est démarré et que les modèles sont téléchargés[/dim]")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Tests interrompus[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Erreur inattendue: {e}[/red]") 