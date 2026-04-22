from fastapi import APIRouter
from app.service.explainer import generate_explanation

router = APIRouter()

@router.post("/explain")
def explain_recommendation(data: dict):

    query = data["query"]
    movie = data["movie"]
    metadata = data.get("metadata", {})

    explanation  = generate_explanation(query, movie, metadata)

    return {
        "movie": movie,
        "explanation": explanation
    }
