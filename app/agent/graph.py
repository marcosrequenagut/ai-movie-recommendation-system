from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.router_node import router_node
from app.agent.nodes import (
    clarify_node,
    recommend_node,
    explain_node,
    format_output_node
)

# Init graph
graph = StateGraph(AgentState)

# Nodes
graph.add_node("router", router_node)
graph.add_node("recommend", recommend_node)
graph.add_node("explain", explain_node)
graph.add_node("clarify", clarify_node)

graph.add_node("format_output_node", format_output_node)

# Entry
graph.set_entry_point("router")

# Routing
graph.add_conditional_edges(
    "router",
    lambda state: state.action,
    {
        "recommend": "recommend",
        "explain": "explain",
        "clarify": "clarify"
    }
)

graph.add_edge("recommend", "format_output_node")
graph.add_edge("explain", "format_output_node")
graph.add_edge("clarify", "format_output_node")

# Final
graph.add_edge("format_output_node", END)

# Compile
app = graph.compile()