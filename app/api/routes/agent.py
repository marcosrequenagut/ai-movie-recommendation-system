from fastapi import APIRouter
from app.agent.agent import run_agent

router =  APIRouter()

@router.post("/agent")
def agent_chat(data: dict):

    user_input = data["message"]

    result = run_agent(user_input)

    return result


