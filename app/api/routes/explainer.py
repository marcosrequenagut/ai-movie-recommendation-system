from fastapi import APIRouter
from app.service.explainer import generate_explanation
from app.agent.state import AgentState

router = APIRouter()

@router.post("/explain")
def explain_recommendation(data: dict):

    state = AgentState(
        query = data["query"]
        movie = data["movie"]
        metadata = data.get("metadata", {})
    )

    explanation  = generate_explanation(state)

    return {
        "movie": state.movie,
        "explanation": explanation
    }
