from app.agent.graph import app
from app.agent.state import AgentState

# This is not LangGraph is the internal API

def agent(user_input, thread_id, filters=None, top_k=5, user_mode="smart"):
    """
    This function is the entry point of the LangGraph system (the bridge between the app and the graph).
    thread_id identifies the conversation - same thread_id = same conversation context.
    """

    # Normalize filters to asure that year_from/year_to are in the filters dictionary
    normalized_filters = {
        **(filters or {}),
        "year_from": (filters or {}).get("year_from", 1900),
        "year_to": (filters or {}).get("year_to", 2100),
    }

    # Input of the graph
    # We have to reset some characteristics of the state like (movies, explanation, message, clarify_count and message) because the checkpoint saves the values 
    # from the previous result, if we don't reset them, they are going to take the values of the previous call and we don't want this.
    state = AgentState(
        raw_query=user_input,
        filters=normalized_filters,
        top_k=top_k,
        user_mode=user_mode,
        movies=[],
        explanation=None,
        message=None,
        clarify_count=0,
        expanded_queries=[]
    )

    # Config tells LangGraph which conversation to recover from SQLite
    config = {"configurable": {"thread_id": thread_id}}

    # Execute the graph with the conversation config
    result = app.invoke(state, config=config)

    # We clean the output to be used by the API
    return {
        "query": result.get("query"),
        "action": result.get("action"),
        "movies": result.get("movies", []),
        "filters": result.get("filters", {}),
        "user_mode": result.get("user_mode"),
        "conversation_history": result.get("conversation_history", []) 
    }
