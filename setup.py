#!/usr/bin/env python3
"""
Script de configuration pour le Multi-Agent System avec Agno
Installe et configure Ollama avec les modèles nécessaires
"""

import subprocess
import sys
import time
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def run_command(command: str, description: str = "") -> bool:
    """Exécute une commande shell avec gestion d'erreur"""
    try:
        if description:
            console.print(f"[blue]🔄 {description}[/blue]")
        
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            console.print(f"[green]✅ {description or 'Commande'} réussie[/green]")
            return True
        else:
            console.print(f"[red]❌ Erreur: {result.stderr}[/red]")
            return False
            
    except subprocess.TimeoutExpired:
        console.print(f"[red]❌ Timeout: {description}[/red]")
        return False
    except Exception as e:
        console.print(f"[red]❌ Erreur: {e}[/red]")
        return False

def check_ollama_installed() -> bool:
    """Vérifie si Ollama est installé"""
    result = subprocess.run("ollama --version", shell=True, capture_output=True)
    return result.returncode == 0

def install_ollama():
    """Installe Ollama selon l'OS"""
    console.print(Panel.fit(
        "[bold blue]🚀 Installation d'Ollama[/bold blue]",
        border_style="blue"
    ))
    
    if sys.platform == "darwin":  # macOS
        console.print("[yellow]📱 Détection de macOS[/yellow]")
        console.print("[dim]Veuillez installer Ollama manuellement depuis: https://ollama.ai[/dim]")
        console.print("[dim]Ou utilisez: brew install ollama[/dim]")
        return False
    elif sys.platform.startswith("linux"):  # Linux
        console.print("[yellow]🐧 Détection de Linux[/yellow]")
        return run_command(
            "curl -fsSL https://ollama.ai/install.sh | sh",
            "Installation d'Ollama sur Linux"
        )
    else:
        console.print("[red]❌ OS non supporté pour l'installation automatique[/red]")
        return False

def pull_models():
    """Télécharge les modèles Ollama nécessaires"""
    console.print(Panel.fit(
        "[bold blue]📥 Téléchargement des modèles[/bold blue]",
        border_style="blue"
    ))
    
    models = [
        "mistral:latest",      # Modèle principal
        "llama3.2:3b",         # Alternative légère
        "phi3:mini",           # Pour le code
    ]
    
    success = True
    for model in models:
        console.print(f"[blue]📦 Téléchargement du modèle: {model}[/blue]")
        if not run_command(f"ollama pull {model}", f"Téléchargement de {model}"):
            console.print(f"[yellow]⚠️ Échec du téléchargement de {model}[/yellow]")
            success = False
        time.sleep(1)  # Pause entre les téléchargements
    
    return success

def install_python_deps():
    """Installe les dépendances Python"""
    console.print(Panel.fit(
        "[bold blue]🐍 Installation des dépendances Python[/bold blue]",
        border_style="blue"
    ))
    
    # Vérifier si uv est disponible
    if subprocess.run("uv --version", shell=True, capture_output=True).returncode == 0:
        return run_command("uv sync", "Installation avec uv")
    else:
        return run_command("pip install -r requirements.txt", "Installation avec pip")

def test_setup():
    """Test la configuration"""
    console.print(Panel.fit(
        "[bold blue]🧪 Test de la configuration[/bold blue]",
        border_style="blue"
    ))
    
    # Test Ollama
    if not run_command("ollama list", "Test d'Ollama"):
        return False
    
    # Test des imports Python
    try:
        import agno
        import ollama
        import typer
        import rich
        console.print("[green]✅ Imports Python OK[/green]")
        return True
    except ImportError as e:
        console.print(f"[red]❌ Import manquant: {e}[/red]")
        return False

def main():
    """Fonction principale de setup"""
    console.print(Panel.fit(
        "[bold green]🤖 Setup Multi-Agent System avec Agno[/bold green]\n"
        "[dim]Configuration automatique d'Ollama et des dépendances[/dim]",
        border_style="green"
    ))
    
    steps = []
    
    # Vérifier Ollama
    if not check_ollama_installed():
        console.print("[yellow]⚠️ Ollama n'est pas installé[/yellow]")
        if not install_ollama():
            console.print("[red]❌ Installation d'Ollama échouée[/red]")
            console.print("[dim]Installez manuellement depuis: https://ollama.ai[/dim]")
            return False
        steps.append("✅ Ollama installé")
    else:
        console.print("[green]✅ Ollama déjà installé[/green]")
        steps.append("✅ Ollama détecté")
    
    # Installer les dépendances Python
    if install_python_deps():
        steps.append("✅ Dépendances Python installées")
    else:
        console.print("[red]❌ Installation des dépendances échouée[/red]")
        return False
    
    # Télécharger les modèles
    if pull_models():
        steps.append("✅ Modèles téléchargés")
    else:
        console.print("[yellow]⚠️ Certains modèles n'ont pas pu être téléchargés[/yellow]")
        steps.append("⚠️ Modèles partiellement téléchargés")
    
    # Test final
    if test_setup():
        steps.append("✅ Configuration testée")
    else:
        console.print("[red]❌ Test de configuration échoué[/red]")
        return False
    
    # Résumé
    console.print(Panel(
        "\n".join(steps) + "\n\n[bold green]🎉 Configuration terminée![/bold green]",
        title="[bold blue]Résumé de l'installation[/bold blue]",
        border_style="green"
    ))
    
    console.print("\n[bold cyan]🚀 Commandes disponibles:[/bold cyan]")
    console.print("[dim]python main.py list-agents[/dim] - Liste les agents")
    console.print("[dim]python main.py chat --agent general[/dim] - Chat avec l'agent général")
    console.print("[dim]python main.py demo[/dim] - Démonstration rapide")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Installation interrompue[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Erreur inattendue: {e}[/red]")
        sys.exit(1) 