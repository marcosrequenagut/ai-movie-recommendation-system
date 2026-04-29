from fastapi import APIRouter
from app.db.connection import get_connection
from app.service.filter import FilterRequest

router = APIRouter()

@router.post("/filter")
def apply_genres_filter(movies, genres):

    conn = get_connection()

    result = filter_movies(
        movies = movies,
        genres = genres,
        conn = conn
    )

    conn.close()
    return result