from langchain_core.tools import tool
import ast
import logging
import os
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_ollama import ChatOllama
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage

# Configuration simple des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Désactiver LangSmith pour éviter les erreurs d'auth
os.environ["LANGCHAIN_TRACING_V2"] = "false"

@tool
def calculator(query: str) -> str: 
    """Use this tool to calculate the result of a mathematical expression."""
    logger.info(f"🧮 Calcul demandé: {query}")
    try:
        # Méthode simple et sécurisée
        result = eval(query, {"__builtins__": {}}, {})
        logger.info(f"✅ Résultat: {result}")
        return str(result)
    except Exception as e:
        error_msg = f"Erreur: {str(e)}"
        logger.error(f"❌ {error_msg}")
        return error_msg

# Initialisation des outils
logger.info("🔧 Initialisation des outils...")
search = DuckDuckGoSearchRun()
tools = [search, calculator]

# Modèle
logger.info("🤖 Initialisation du modèle...")
model = ChatOllama(model="mistral", temperature=0.1).bind_tools(tools)

class State(TypedDict):
    messages: Annotated[list, add_messages]

def model_node(state: State) -> State:
    logger.info(f"🤖 Appel du modèle...")
    res = model.invoke(state["messages"])
    
    # Log des outils appelés
    if hasattr(res, 'tool_calls') and res.tool_calls:
        tools_called = [tc['name'] for tc in res.tool_calls]
        logger.info(f"🛠️ Outils appelés: {tools_called}")
    
    logger.info(f"✅ Réponse reçue")
    return {"messages": res}

# Construction du graphe
logger.info("🏗️ Construction du graphe...")
builder = StateGraph(State) 
builder.add_node("model", model_node) 
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "model")
builder.add_conditional_edges("model", tools_condition)
builder.add_edge("tools", "model")

graph = builder.compile()

# Test
input_data = {
    "messages": [
        HumanMessage("combien font 2+2?")
    ]
}

logger.info("🚀 Exécution...")
result = graph.invoke(input_data)

print("\n" + "="*50)
print("RÉPONSE:")
print("="*50)
print(result["messages"][-1].content)
print("="*50)


