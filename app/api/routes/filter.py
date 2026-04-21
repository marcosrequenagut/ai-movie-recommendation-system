from fastapi import APIRouter
from app.db.connection import get_connection
from app.service.filter import FilterRequest

router = APIRouter()

@router.post("/filter")
def filter_movies(request: FilterRequest):

    conn = get_connection()
    result = filter_movies(request, conn)
    conn.close()

    return result