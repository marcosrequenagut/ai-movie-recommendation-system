from ..embeddings.service import embed_query
from ..retrieval.retrieval_service import retrieve_movies
from ..recommender.ranking.ranking_service import rank_movies

def recommend_pipeline(query, top_k=5, allowed_ids=None):

    # 1. Encoding the query into an embedding
    query_embedding = embed_query(query)

    # 2. Retrieval (candidates)
    candidates = retrieve_movies(
        query_embedding=query_embedding,
        top_k=top_k,
        allowed_ids=allowed_ids
    )

    # Ranking (final decision)
    ranked_movies = rank_movies(candidates)

    # Return the top-K final movies
    return ranked_movies[:top_k]
