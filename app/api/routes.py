from fastapi import APIRouter
from pydantic import BaseModel
from app.recommender.recommender import get_recommended_movies

router = APIRouter()

class RecommendationRequest(BaseModel):
    query: str
    top_k: int = 10

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/recommend")
def recommend(request: RecommendationRequest):
    results = get_recommended_movies(request.query, request.top_k)
    return {
        "query": request.query,
        "results": [
            {
                "id": r[0],
                "title": r[1],
                "content": r[2],
                "score": float(r[3])
            } for r in results
        ]
    }