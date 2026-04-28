from ..embeddings.service import embed_query
from ..retrieval.retrieval_service import retrieve_movies
from ..recommender.ranking.ranking_service import rank_movies

def recommend_pipeline(query, allowed_ids=None, top_k=5):

    # 1. Encoding
    query_embedding = embed_query(query)

    # 2. Retrieval (candidates)
    candidates = retrieve_movies(
        embedding=query_embedding,
        allowed_ids=allowed_ids,
        top_k=top_k)
    
    # Ranking (final decision)
    ranked_movies = rank_movies(candidates)

    # Return the top-K final movies
    return ranked_movies[:top_k]