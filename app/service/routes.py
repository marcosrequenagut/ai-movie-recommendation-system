from fastapi import APIRouter
from app.db.connection import get_connection
from app.service.filter import FilterRequest

router = APIRouter()

@router.post("/filter")
def filter_movies(request: FilterRequest):

    """Filters movies based on genre, minimum rating, and release year range.
    Args:
        request (FilterRequest): The filter criteria including genre, minimum rating, and release year range.
    Returns:
        list[int]: A list of movie IDs that match the filter criteria."""

    conn = get_connection()
    cur = conn.cursor()

    sql_query = """
        SELECT id, title, content
        FROM movies
        WHERE genres && %s::text[]
          AND weighted_rating >= %s
          AND release_year BETWEEN %s AND %s;
    """

    params = [request.genres, request.min_rating, request.year_from, request.year_to]

    cur.execute(sql_query, params)
    results = cur.fetchall()
    
    cur.close()
    conn.close()

    # We will return only the ids because is the PK of the table and we are just filtering it
    return [r[0] for r in results]
