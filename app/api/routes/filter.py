from fastapi import APIRouter
from app.db.connection import get_connection
from app.service.filter import FilterRequest, filter_movies

router = APIRouter()

@router.post("/filter")
def apply_genres_filter(data: FilterRequest):
    """This endpoint call the filter_movies to use the filters introduced by the user."""

    conn = get_connection()

    try:
        result = filter_movies(data, conn)   
        return {"movies": result}

    finally:
        conn.close()