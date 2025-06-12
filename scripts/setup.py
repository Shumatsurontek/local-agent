#!/usr/bin/env python3
"""
Setup script for the Multi-Agent System
Installs and configures Ollama with the necessary models
"""

import subprocess
import sys
import time
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from utils.model_utils import check_ollama_connection, list_available_models

console = Console()

def run_command(command: str, description: str = "") -> bool:
    """Execute a shell command with error handling"""
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
            console.print(f"[green]✅ {description or 'Command'} successful[/green]")
            return True
        else:
            console.print(f"[red]❌ Error: {result.stderr}[/red]")
            return False
            
    except subprocess.TimeoutExpired:
        console.print(f"[red]❌ Timeout: {description}[/red]")
        return False
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        return False

def check_ollama_installed() -> bool:
    """Check if Ollama is installed"""
    result = subprocess.run("ollama --version", shell=True, capture_output=True)
    return result.returncode == 0

def install_ollama():
    """Install Ollama based on the OS"""
    console.print(Panel.fit(
        "[bold blue]🚀 Installing Ollama[/bold blue]",
        border_style="blue"
    ))
    
    if sys.platform == "darwin":  # macOS
        console.print("[yellow]📱 macOS detected[/yellow]")
        console.print("[dim]Please install Ollama manually from: https://ollama.ai[/dim]")
        console.print("[dim]Or use: brew install ollama[/dim]")
        return False
    elif sys.platform.startswith("linux"):  # Linux
        console.print("[yellow]🐧 Linux detected[/yellow]")
        return run_command(
            "curl -fsSL https://ollama.ai/install.sh | sh",
            "Installing Ollama on Linux"
        )
    else:
        console.print("[red]❌ OS not supported for automatic installation[/red]")
        return False

def pull_models():
    """Download necessary Ollama models"""
    console.print(Panel.fit(
        "[bold blue]📥 Downloading models[/bold blue]",
        border_style="blue"
    ))
    
    # Check which models are already available
    available_models = [model["name"] for model in list_available_models()]
    
    required_models = [
        "mistral:latest",      # Main model
        "llama3.2:3b",         # Lightweight alternative
        "phi3:mini",           # For specific tasks
    ]
    
    success = True
    for model in required_models:
        if model in available_models:
            console.print(f"[green]✅ Model {model} already available[/green]")
            continue
            
        console.print(f"[blue]📦 Downloading model: {model}[/blue]")
        if not run_command(f"ollama pull {model}", f"Downloading {model}"):
            console.print(f"[yellow]⚠️ Failed to download {model}[/yellow]")
            success = False
        time.sleep(1)  # Pause between downloads
    
    return success

def install_python_deps():
    """Install Python dependencies"""
    console.print(Panel.fit(
        "[bold blue]🐍 Installing Python dependencies[/bold blue]",
        border_style="blue"
    ))
    
    # Check if uv is available
    if subprocess.run("uv --version", shell=True, capture_output=True).returncode == 0:
        return run_command("uv sync", "Installing with uv")
    else:
        return run_command("pip install -e .", "Installing with pip")

def test_setup():
    """Test the configuration"""
    console.print(Panel.fit(
        "[bold blue]🧪 Testing configuration[/bold blue]",
        border_style="blue"
    ))
    
    # Test Ollama
    if not check_ollama_connection():
        console.print("[red]❌ Ollama connection test failed[/red]")
        return False
    
    console.print("[green]✅ Ollama connection OK[/green]")
    
    # Test Python imports
    try:
        import agno
        import ollama
        import streamlit
        import fastapi
        console.print("[green]✅ Python imports OK[/green]")
        return True
    except ImportError as e:
        console.print(f"[red]❌ Missing import: {e}[/red]")
        return False

def main():
    """Main setup function"""
    console.print(Panel.fit(
        "[bold green]🤖 Multi-Agent System Setup[/bold green]\n"
        "[dim]Automatic configuration of Ollama and dependencies[/dim]",
        border_style="green"
    ))
    
    steps = []
    
    # Check Ollama
    if not check_ollama_installed():
        console.print("[yellow]⚠️ Ollama is not installed[/yellow]")
        if not install_ollama():
            console.print("[red]❌ Ollama installation failed[/red]")
            console.print("[dim]Install manually from: https://ollama.ai[/dim]")
            return False
        steps.append("✅ Ollama installed")
    else:
        console.print("[green]✅ Ollama already installed[/green]")
        steps.append("✅ Ollama detected")
    
    # Install Python dependencies
    if install_python_deps():
        steps.append("✅ Python dependencies installed")
    else:
        console.print("[red]❌ Python dependencies installation failed[/red]")
        return False
    
    # Download models
    if pull_models():
        steps.append("✅ Models downloaded")
    else:
        console.print("[yellow]⚠️ Some models could not be downloaded[/yellow]")
        steps.append("⚠️ Models partially downloaded")
    
    # Final test
    if test_setup():
        steps.append("✅ Configuration tested")
    else:
        console.print("[red]❌ Configuration test failed[/red]")
        return False
    
    # Summary
    console.print(Panel(
        "\n".join(steps) + "\n\n[bold green]🎉 Setup complete![/bold green]",
        title="[bold blue]Installation Summary[/bold blue]",
        border_style="green"
    ))
    
    console.print("\n[bold cyan]🚀 Available commands:[/bold cyan]")
    console.print("[dim]python -m scripts.run api[/dim] - Start the API server")
    console.print("[dim]python -m scripts.run ui[/dim] - Start the Streamlit UI")
    console.print("[dim]python -m scripts.run both[/dim] - Start both services")
    console.print("[dim]streamlit run ui/agent_chat.py[/dim] - Direct Streamlit launch")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Installation interrupted[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {e}[/red]")
        sys.exit(1) 