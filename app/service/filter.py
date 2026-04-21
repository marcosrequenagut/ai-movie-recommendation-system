from pydantic import BaseModel, Field

class FilterRequest(BaseModel):
    genres: list[str] = Field(default_factory=list)
    min_rating: float = 0.0
    year_from: int = 1900
    year_to: int = 2100


def filter_movies(request, conn):

    cur = conn.cursor()

    sql_query = """
        SELECT id, title, content
        FROM movies
        WHERE genres && %s::text[]
          AND weighted_rating >= %s
          AND release_year BETWEEN %s AND %s;
    """

    params = [
        request.genres,
        request.min_rating,
        request.year_from,
        request.year_to
    ]

    cur.execute(sql_query, params)
    results = cur.fetchall()

    cur.close()

    return [r[0] for r in results]