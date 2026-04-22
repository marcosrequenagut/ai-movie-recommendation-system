from ..db.connection import get_connection
from ..embeddings.service import embed_query
from ..repositories.movie_repository import search_movies_by_embedding


def get_recommended_movies(query, top_k=10, allowed_ids=None):

    # 1. Conection
    conn = get_connection()

    try:
        # 2. Embedding
        query_embedding = embed_query(query)

        # 3. Search
        results = search_movies_by_embedding(
            conn=conn,
            embedding=query_embedding,
            allowed_ids=allowed_ids,
            top_k=top_k
        )

        return results

    finally:
        conn.close()