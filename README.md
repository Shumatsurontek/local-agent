# Local Agent

A local AI agent built with LangChain and LangGraph that combines web search capabilities with mathematical computation. The agent uses Ollama's Mistral model to process queries and can autonomously decide when to search the web or perform calculations.

## Features

- **Web Search**: Uses DuckDuckGo search to find real-time information
- **Mathematical Calculations**: Safely evaluates mathematical expressions
- **Autonomous Tool Selection**: Intelligently chooses between search and calculation based on the query
- **Local LLM**: Runs entirely locally using Ollama's Mistral model
- **Graph-based Architecture**: Built with LangGraph for robust conversation flow

## Architecture

The agent uses a graph-based architecture with two main nodes:
- **Model Node**: Processes user input and decides which tools to use
- **Tools Node**: Executes the selected tools (search or calculator)

The system maintains conversation state and can handle multi-turn interactions.

## Prerequisites

- Python 3.13+
- [Ollama](https://ollama.ai/) installed and running
- Mistral model pulled in Ollama: `ollama pull mistral`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd local-agent
```

2. Install dependencies using uv (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
```

3. Ensure Ollama is running and has the Mistral model:
```bash
ollama serve
ollama pull mistral
```

## Usage

### Basic Usage

The main functionality is in `main.py`. To use the agent, uncomment the example code at the bottom of the file and run:

```python
from langchain_core.messages import HumanMessage

# Create an input for the graph
input_data = {
    "messages": [
        HumanMessage("What was the age of the youngest person to win a Nobel Prize?")
    ]
}

# Pass the input to the graph and invoke it
result = graph.invoke(input_data)
print(result["messages"][-1].content)
```

### Example Queries

The agent can handle various types of queries:

**Web Search Queries:**
- "What's the latest news about AI?"
- "Who won the Nobel Prize in Physics in 2023?"
- "What's the weather like in Tokyo?"

**Mathematical Calculations:**
- "Calculate 15 * 23 + 45"
- "What is 2^10?"
- "Solve (100 + 50) / 3"

**Mixed Queries:**
- "How many days until Christmas 2024 and calculate 365 - 30"
- "What's the population of Tokyo and divide it by 1000"

## Project Structure

```
local-agent/
├── main.py              # Main agent implementation
├── pyproject.toml       # Project configuration
├── requirements.txt     # Python dependencies
├── uv.lock             # Dependency lock file
├── README.md           # This file
└── .venv/              # Virtual environment
```

## Dependencies

- **langchain**: Core LangChain framework
- **langgraph**: Graph-based conversation flow
- **langchain-ollama**: Ollama integration for local LLMs
- **langchain-community**: Community tools including DuckDuckGo search
- **duckduckgo-search**: Web search functionality

## Configuration

The agent is configured with:
- **Model**: Mistral via Ollama
- **Temperature**: 0.1 (for more deterministic responses)
- **Tools**: Web search and calculator

## Development

To extend the agent with new tools:

1. Create a new tool function using the `@tool` decorator
2. Add it to the `tools` list
3. The agent will automatically learn to use it

Example:
```python
@tool
def weather_tool(location: str) -> str:
    """Get weather information for a location."""
    # Implementation here
    pass

tools = [search, calculator, weather_tool]
```

## Visualization

The project includes commented code to generate a visual representation of the agent's graph structure:

```python
with open("graph.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())
```

## Troubleshooting

**Common Issues:**

1. **Ollama not running**: Ensure Ollama service is started with `ollama serve`
2. **Mistral model not found**: Pull the model with `ollama pull mistral`
3. **Import errors**: Ensure all dependencies are installed in your virtual environment

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
