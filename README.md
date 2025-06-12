# Multi-Agent System with Agno

A powerful multi-agent system built with the **Agno framework**, featuring specialized agents for different tasks including web search, financial analysis, code execution, and system administration.

## Features

- **🤖 Multiple Specialized Agents**: General, Search, Finance, Code, and System agents
- **🔧 Agno Framework**: Built on the modern Agno Agent framework
- **🦙 Ollama Integration**: Local LLM inference with multiple models (Mistral, Llama3.2, Phi3)
- **🌐 FastAPI Backend**: RESTful API for agent interactions
- **🎨 Streamlit UI**: Beautiful web interface for chat interactions
- **👥 Team Collaboration**: Multi-agent teams with coordination capabilities
- **🏗️ Extensible Architecture**: Easy to add new agents and tools

## Quick Start

### 1. Automatic Setup
```bash
# Full setup with dependencies and models
make setup

# Or manually
python -m scripts.setup
```

### 2. Manual Setup
```bash
# Install dependencies
pip install -e .

# Start Ollama (if not running)
ollama serve

# Download required models
ollama pull mistral:latest
ollama pull llama3.2:3b
ollama pull phi3:mini
```

### 3. Run the System
```bash
# Start both API and UI
make run
# or
python -m scripts.run both

# Start only API
make run-api

# Start only UI  
make run-ui
```

### 4. Access the Application
- **Streamlit UI**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## Architecture

The system follows the **official Agno Agent App architecture**:

```
local-agent/
├── agents/           # Individual agent definitions
│   ├── general.py    # General conversation agent
│   ├── search.py     # Web search with DuckDuckGo
│   ├── finance.py    # Financial analysis with YFinance
│   ├── code.py       # Python code execution
│   ├── system.py     # System administration
│   └── settings.py   # Model configuration
├── api/              # FastAPI backend
│   ├── main.py       # API application
│   ├── agents.py     # Agent endpoints
│   └── teams.py      # Team collaboration endpoints
├── ui/               # Streamlit frontend
│   └── agent_chat.py # Chat interface
├── teams/            # Multi-agent teams
│   └── research.py   # Collaborative research team
├── utils/            # Shared utilities
│   ├── logging_config.py
│   └── model_utils.py
├── workspace/        # Agno workspace configuration
│   ├── settings.py   # Workspace settings
│   └── dev_resources.py
└── scripts/          # Helper scripts
    ├── setup.py      # Automatic setup
    └── run.py        # Service runner
```

## Available Agents

### 🤖 General Agent
- Natural conversation handling
- General assistance and information
- **Model**: Configurable (default: mistral:latest)

### 🔍 Search Agent  
- Web search using DuckDuckGo
- Real-time information retrieval
- **Tools**: DuckDuckGo search
- **Model**: llama3.2:3b

### 💰 Finance Agent
- Stock price analysis
- Financial data retrieval
- Market information
- **Tools**: YFinance
- **Model**: mistral:latest

### 💻 Code Agent
- Python code execution
- Mathematical calculations
- Programming assistance
- **Tools**: Python REPL, Calculator
- **Model**: llama3.2:latest

### ⚙️ System Agent
- Shell command execution
- System administration
- File management
- **Tools**: Shell execution
- **Model**: phi3:mini

### 👥 Research Team
- Collaborative multi-agent team
- Combines search, analysis, and synthesis
- **Members**: Search + Finance + General agents
- **Mode**: Coordinate for collaborative work

## API Endpoints

### Health & Status
- `GET /health` - Health check
- `GET /` - Root endpoint

### Agents
- `GET /agents` - List all agents
- `POST /agents/{agent_id}/chat` - Chat with specific agent

### Teams
- `GET /teams` - List all teams  
- `POST /teams/{team_id}/chat` - Chat with agent team

## Configuration

### Model Configuration
Edit `agents/settings.py` to configure models:

```python
MODEL_CONFIG = {
    "general": "mistral:latest",
    "search": "llama3.2:3b", 
    "finance": "mistral:latest",
    "code": "llama3.2:latest",
    "system": "phi3:mini"
}
```

### Workspace Settings
Edit `workspace/settings.py` for workspace configuration:

```python
ws_settings = WorkspaceSettings(
    ws_name="local-agent-agno",
    api_port=8000,
    streamlit_port=8501,
    # ... other settings
)
```

## Development Commands

```bash
# Setup and installation
make setup          # Full setup
make install        # Install dependencies only

# Running services
make run           # Start both API and UI
make run-api       # Start API only
make run-ui        # Start UI only

# Development
make test          # Run tests
make lint          # Run linter
make format        # Format code
make clean         # Clean temporary files

# Ollama management
make ollama-status # Check Ollama status
make ollama-models # List available models
```

## Dependencies

### Core Framework
- **Agno**: Modern agent framework
- **Ollama**: Local LLM inference
- **FastAPI**: Web API framework  
- **Streamlit**: Web UI framework

### Agent Tools
- **DuckDuckGo**: Web search
- **YFinance**: Financial data
- **Rich**: Terminal formatting

### Development
- **Uvicorn**: ASGI server
- **Pytest**: Testing framework
- **Ruff**: Code linting and formatting

## Adding New Agents

1. **Create Agent File**: Add new agent in `agents/`
2. **Define Tools**: Add required tools to the agent
3. **Update Settings**: Add model configuration
4. **Register in API**: Add endpoints in `api/agents.py`
5. **Update UI**: Add to agent selection in UI

Example agent structure:
```python
from agno import Agent
from agno.models.ollama import OllamaChat

agent = Agent(
    name="MyAgent",
    model=OllamaChat(id="mistral:latest"),
    description="Agent description",
    instructions="Detailed instructions",
    tools=[my_tool_function]
)
```

## Example Usage

### Via Streamlit UI
1. Open http://localhost:8501
2. Select an agent or team
3. Start chatting!

### Via API
```bash
# Chat with search agent
curl -X POST "http://localhost:8000/agents/search/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Search for latest AI news"}'

# Chat with research team
curl -X POST "http://localhost:8000/teams/research/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Research the current state of renewable energy"}'
```

## Production Deployment

For production deployment with the full Agno stack:

1. **Setup PostgreSQL database**
2. **Configure environment variables**
3. **Update workspace settings**
4. **Deploy with your preferred method** (Docker, Kubernetes, etc.)

The system is designed to work seamlessly with the Agno framework's production features including database persistence, user management, and scalable deployment.
