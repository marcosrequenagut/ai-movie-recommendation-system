from app.agent.graph import app
from app.agent.state import AgentState

def agent(user_input, filters=None, top_k=5):

    state = AgentState(
        query=user_input,
        filters=filters,
        top_k=top_k
    )

    result = app.invoke(state)

    return {
        "query": result.get("query"),
        "action": result.get("action"),
        "movies": result.get("movies", []) 
    }