from langchain_core.tools import tool
import ast
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_ollama import ChatOllama
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage

# Create a calculator function
@tool
def calculator(query: str) -> str: 
  # Explain the aim of this function 
  """Use this tool to calculate the result of a mathematical expression."""
  # Use literal_eval to safely evaluate mathematical expressions provided in string format.
  return ast.literal_eval(query)

# Instantiate the object.
search = DuckDuckGoSearchRun()

# Define a variable to hold all the tools we'll use
tools = [search, calculator]

# Create a large model
model = ChatOllama(model="mistral", temperature=0.1).bind_tools(tools)

# Create a State object that acts as the system's memory
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Build the model node
def model_node(state: State) -> State:
    res = model.invoke(state["messages"])
    return {"messages": res}

# Initialize the graph
builder = StateGraph(State) 

# Build the nodes
builder.add_node("model", model_node) 
builder.add_node("tools", ToolNode(tools))

# Add the edges
builder.add_edge(START, "model")
builder.add_conditional_edges("model", tools_condition)
builder.add_edge("tools", "model")

graph = builder.compile()

"""
with open("graph.png", "wb") as f:
  f.write(graph.get_graph().draw_mermaid_png())

"""
"""
# Create an input for the graph
input = {
    "messages": [
        HumanMessage(
            "What was the age of the youngest person to win a Nobel Prize?"
        )
    ]
}


# Pass the input to the graph and invoke the graph
result = graph.invoke(input)
print(result)
print("--------------The AI Agent's Answer------------------")
print(result["messages"][-1].content)

"""


