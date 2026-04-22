from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List

from app.recommender.recommender import get_recommended_movies
from app.service.filter import FilterRequest, filter_movies
from app.service.explainer import generate_explanation
from app.db.connection import get_connection

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

    conn = get_connection()

    filtered_ids = filter_movies(
        FilterRequest(
            genres=request.genres,
            min_rating=request.min_rating,
            year_from=request.year_from,
            year_to=request.year_to
        ),
        conn
    )

    results = get_recommended_movies(
        query=request.query,
        top_k=request.top_k,
        allowed_ids=filtered_ids
    )

    conn.close()

    # Introduce the explaination of the most recommended movie using a LLM called Ollama
    score_most_recommended_movie = 0
    for r in results:
        score = float(r[3])
        if score > score_most_recommended_movie:
            # Create a metadata using the most recommended movie
            dict_metadata = {
                "title": r[1],
                "genres": r[4],
                "overview": r[5],
                "release_year": r[6],
                "vote_average": r[7],
                "popularity": r[8],
            }

            score_most_recommended_movie = score

    explanation = generate_explanation(
        query = request.query,
        movie = dict_metadata["title"],
        metadata = dict_metadata
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
        ],
        "explanation": explanation
    }