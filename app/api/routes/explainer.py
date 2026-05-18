from fastapi import APIRouter
from app.service.explainer import generate_explanation
from app.agent.state import AgentState

router = APIRouter()

@router.post("/explain")
def explain_recommendation(data: dict):

    state = AgentState(
        query = data["query"],
        movies= data["movies"],
        metadata = data.get("metadata", {})
    )

    explanation  = generate_explanation(state)

    return {
        "movies": state.movies,
        "explanation": explanation
    }
