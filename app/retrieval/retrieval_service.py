from app.db.connection import get_connection
from app.repositories.movie_repository import search_movies_by_embedding
from app.embeddings.service import embed_query

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

def retrieve_movies_multi(queries: list, top_k=5, allowed_ids=None):
    """
    Multi-query retrieval layer:
    - Generates an embedding for each query variant.
    - Executes one vector search per query.
    - Meges and deduplicates results by movie id.
    - Returns a flat deduplicated list of candidades.
    
    Deduplication keeps the best result (lowest distance) for each movie.
    """

    conn = get_connection()
    internal_top = top_k * 5

    try:
        seen_ids = {} # id -> best result (lowest distance = x[3])

        for query in queries:
            # Generate embedding for this variant
            embedding = embed_query(query)

            # Search in pgvector
            results = search_movies_by_embedding(
                conn=conn,
                embedding=embedding,
                allowed_ids=allowed_ids,
                top_k=internal_top
            )

            # Deduplicates keeping best distance per movie
            for movie in results:
                movie_id = movie[0]
                distance = float(movie[3])

                if movie_id not in seen_ids:
                    seen_ids[movie_id] = movie
                else: 
                    # Keep the resul with the lowest distance
                    if distance < float(seen_ids[movie_id][3]):
                        seen_ids[movie_id] = movie

        deduplicated = list(seen_ids.values())

        print(f"\nMULTI RETREIVAL: {len(queries)} queries -> {len(deduplicated)} unique candidates")

        return deduplicated
    
    finally:
        conn.close()