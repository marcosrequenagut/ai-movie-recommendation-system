from app.agent.graph import app
from app.agent.state import AgentState

def agent(user_input, filters=None, top_k=5, user_mode="smart"):

    state = AgentState(
        query=user_input,
        filters={"genres": filters} if filters else None,
        top_k=top_k,
        user_mode=user_mode
    )

    result = app.invoke(state)

    return {
        "query": result.get("query"),
        "action": result.get("action"),
        "movies": result.get("movies", []) 
    }