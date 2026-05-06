from app.db.connection import get_connection
from app.repositories.movie_repository import search_movies_by_embedding


def retrieve_movies(query_embedding, top_k=5, allowed_ids=None):

    """
    Unic retrieval layer:
    - Connects to the DB
    - Execute the vectorial search
    - Returns the candidates movies
    """

    # 1. Conection
    conn = get_connection()

    try:

        # 2. Search
        results = search_movies_by_embedding(
            conn=conn,
            embedding=query_embedding,
            allowed_ids=allowed_ids,
            top_k=top_k
        )

        return results

    finally:
        conn.close()