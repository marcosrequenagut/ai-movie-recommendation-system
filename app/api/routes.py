from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.recommender.recommender import get_recommended_movies
from app.service.routes import filter_movies
from app.service.filter import FilterRequest
from typing import List

router = APIRouter()

class RecommendationRequest(BaseModel):
    query: str
    top_k: int = 5
    genres: List[str] = Field(default_factory=list)
    min_rating: float = 0.0
    year_from: int = 1900
    year_to: int = 2100

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/recommend")
def recommend(request: RecommendationRequest):

    # First we filter the movies based on the user preferences using the filter endpoint.
    filtered_ids = filter_movies(
        FilterRequest(
            genres=request.genres,
            min_rating=request.min_rating,
            year_from=request.year_from,
            year_to=request.year_to
        )
    )


    # Then we get the recommended movies based on the query and the filtered ids.
    results = get_recommended_movies(
        query=request.query,
        top_k=request.top_k,
        allowed_ids=filtered_ids
    )

    return {
        "query": request.query,
        "results": [
            {
                "id": r[0],
                "title": r[1],
                "content": r[2],
                "score": float(r[3]),
                "genres": r[4]
            } for r in results
        ]
    }