from fastapi import APIRouter
from app.agent.agent import agent
from app.agent.agent_schema import AgentRequest

router =  APIRouter()

@router.post("/agent")
def agent_chat(data: AgentRequest):

    result = agent(
        user_input = data.message,
        top_k = data.top_k,
        filters = data.genres,
        user_mode = data.user_mode or "smart"
    )

    print("AGENT RESULT:", result)

    return {
        "query": result.get("query"),
        "action": result.get("action"),
        "movies": result.get("movies", [])
    }


