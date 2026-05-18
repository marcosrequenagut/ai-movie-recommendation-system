from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from pathlib import Path
import sqlite3
from app.agent.state import AgentState
from app.agent.router_node import router_node
from app.agent.nodes import (
    clarify_node,
    recommend_node,
    explain_node,
    format_output_node,
    final_clarify_node,
    semantic_filter_node,
    query_expansion_node,
    contextualize_query_node
)

# Checkpointer - save the state on the disk between API calls
DB_PATH = Path(__file__).resolve().parents[2] / "data_procesing" / "data" / "memory" / "memory.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
checkpointer = SqliteSaver(conn)


# Init the graph (all the system works with the same state)
graph = StateGraph(AgentState)

# Nodes (each node is a function of IA or logic)
graph.add_node("contextualize", contextualize_query_node)
graph.add_node("router", router_node)
graph.add_node("semantic_filter", semantic_filter_node)
graph.add_node("query_expansion", query_expansion_node)
graph.add_node("recommend", recommend_node)
graph.add_node("explain", explain_node)
graph.add_node("clarify", clarify_node) # Loop to the router until it choses a different option than clarify
graph.add_node("final_clarify", final_clarify_node)
graph.add_node("format_output_node", format_output_node)

graph.set_entry_point("contextualize")

graph.add_edge("contextualize", "semantic_filter") 
graph.add_edge("semantic_filter", "router") # The preprocess is always connected to the router

def router_selector(state: AgentState):
    """This function returns the action if it is a valid action, else it returns "clarify"""

    if state.action == "final_clarify":
        return "final_clarify"
    
    return state.action if state.action in {"recommend", "explain", "clarify"} else "clarify"

# Routing (conditional routing).
# The router_node produce a dictionary (state) where one of the keys is the "action"
graph.add_conditional_edges(
    "router",
    router_selector,
    {
        "recommend": "query_expansion", # If the action is recommend, it leads to the recommend node
        "explain": "explain", # If the action is explain, it leads to the explain node
        "clarify": "clarify", # If the action is clarify, it leads to the clarify node
        "final_clarify": "final_clarify"
    }
)

graph.add_edge("query_expansion", "recommend") # Query expansion is connected only to the reccommend node, because it will be executed only of the action is "recommend"

graph.add_edge("clarify", "router") # This edge is the one who creates the loop in the clarify node.It always returns to the router node

graph.add_edge("recommend", "format_output_node")
graph.add_edge("explain", "format_output_node")
graph.add_edge("final_clarify", "format_output_node")
graph.add_edge("format_output_node", END) # Final (Execution stops here)

# Compile using the checkpointer
app = graph.compile(checkpointer=checkpointer)


# Save the graph as a png document to better understand it
graph_png = app.get_graph().draw_mermaid_png()

output_path = Path(__file__).resolve().parents[2] / "data_procesing" / "data" / "graph.png"
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "wb") as f:
    f.write(graph_png)