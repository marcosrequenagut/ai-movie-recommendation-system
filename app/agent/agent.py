from app.agent.graph import app
from app.agent.state import AgentState

# This is not LangGraph is the internal API

def agent(user_input, filters=None, top_k=5, user_mode="smart"):
    """ This function is the entry point of the LangGraph system (the bridge between the app and the graph)."""

    # Input of the graph
    state = AgentState(
        query=user_input,
        filters=filters,
        top_k=top_k,
        user_mode=user_mode
    )

    # Execute the graph (router + nodes ...) app is defined in the graph.py script, where it is compiled: app = graph.compile()
    result = app.invoke(state)

    # We clean the output to be used by the API
    return {
        "query": result.get("query"),
        "action": result.get("action"),
        "movies": result.get("movies", []) 
    }