from langgraph.graph import StateGraph, END
from pathlib import Path
from app.agent.state import AgentState
from app.agent.router_node import router_node
from app.agent.nodes import (
    clarify_node,
    recommend_node,
    explain_node,
    format_output_node,
    final_clarify_node,
    semantic_filter_node
)


# Init graph (all the system works with the same state)
graph = StateGraph(AgentState)

# Nodes (each node is a function of IA or logic)
graph.add_node("router", router_node)
graph.add_node("semantic_filter", semantic_filter_node)
graph.add_node("recommend", recommend_node)
graph.add_node("explain", explain_node)
graph.add_node("clarify", clarify_node) # Loop to the router until it choses a different option than clarify
graph.add_node("final_clarify", final_clarify_node)
graph.add_node("format_output_node", format_output_node)

# Entry point of the system (we start by the router, that is goin to take the decision of what node is going to be executed)
graph.set_entry_point("router")

def router_selector(state: AgentState):
    """This function returns the action if it is a valid action, else it returns "clarify"""

    # If the semantic_filter node has not been executed yet, it will be executed. If it has already been executed, it will be skipped.
    if not state.semantic_flag:
        return "semantic_filter"
    
    if state.action == "final_clarify":
        return "final_clarify"
    
    return state.action if state.action in {"recommend", "explain", "clarify"} else "clarify"

# Routing (conditional routing).
# After the router node runs (user_input -> router_node -> update_state -> take decision -> conditional edge), decide where to go next based on state.action
# The router_node produce a dictionary (state) where one of the keys is the "action"
graph.add_conditional_edges(
    "router",
    router_selector,
    {
        "semantic_filter": "semantic_filter",
        "recommend": "recommend", # If the action is recommend, it leads to the recommend node
        "explain": "explain", # If the action is explain, it leads to the explain node
        "clarify": "clarify", # If the action is clarify, it leads to the clarify node
        "final_clarify": "final_clarify"
    }
)

# It is necessary to connect all the nodes to the "output node". All nodes produce intermediate results, one final node formatter cleans everything. This is done to enforce consistency.
graph.add_edge("recommend", "format_output_node")
graph.add_edge("explain", "format_output_node")
graph.add_edge("final_clarify", "format_output_node")
graph.add_edge("clarify", "router") # This edge is the one who creates the loop in the clarify node
graph.add_edge("semantic_filter", "router") # When this node is executed, it returns to the router and it won't be execute then, it will be skiped. 
# Final (Execution stops here)
graph.add_edge("format_output_node", END)

# Compile (turns the graph definition into an executable system)
app = graph.compile()


# Save the graph as a png document to better understand it
graph_png = app.get_graph().draw_mermaid_png()

output_path = Path(__file__).resolve().parents[2] / "data_procesing" / "data" / "graph.png"
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "wb") as f:
    f.write(graph_png)