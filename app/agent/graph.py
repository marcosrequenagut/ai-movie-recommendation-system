from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.router_node import router_node
from app.agent.nodes import (
    clarify_node,
    recommend_node,
    explain_node,
    format_output_node
)

# This is the complete architecture of the agent. Here we define what nodes exist, how are they connected, how we decided which node execute and
# the workflow of execution

#      START
#        ▼
# ┌────────────────┐
# │    router      │  ← LLM decide the action
# └──────┬─────────┘
#        │(state.action)
#        │
#   |────────|────────────|
#   ▼        ▼            ▼
# recommend  explain  clarify
#   │        │        │
#   └────┬───┴───┬────┘
#        ▼
# format_output_node
#        ▼
#       END


# Init graph (all the system works with the same state)
graph = StateGraph(AgentState)

# Nodes (each node is a function of IA or logic)
graph.add_node("router", router_node)
graph.add_node("recommend", recommend_node)
graph.add_node("explain", explain_node)
graph.add_node("clarify", clarify_node)
graph.add_node("format_output_node", format_output_node)

# Entry point of the system (we start by the router, that is goin to take the decision of what node is going to be executed)
graph.set_entry_point("router")

def router_selector(state: AgentState):
    """This function returns the action if it is a valid action, else it returns "clarify"""
    return state.action if state.action in {"recommend", "explain", "clarify"} else "clarify"


# Routing (conditional routing).
# After the router node runs (user_inpur -> router_node -> update_state -> take decision -> conditional edge), decide where to go next based on state.action
# The router_node produce a dictionary (state) where one of the keys is the "action"
graph.add_conditional_edges(
    "router",
    router_selector,
    {
        "recommend": "recommend", # If the action is recommend, it leads to the recommend node
        "explain": "explain", # If the action is explain, it leads to the explain node
        "clarify": "clarify" # If the action is clarify, it leads to the clarify node
    }
)

# It is necessary to connect all the nodes to the "output node". All nodes produce intermediate results, one final node formatter cleans everything. This is done to enforce consistency.
graph.add_edge("recommend", "format_output_node")
graph.add_edge("explain", "format_output_node")
graph.add_edge("clarify", "format_output_node")

# Final (Execution stops here)
graph.add_edge("format_output_node", END)

# Compile (turns the graph definition into an executable system)
app = graph.compile()