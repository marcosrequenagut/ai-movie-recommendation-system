from app.agent.state import AgentState
from app.db.connection import get_connection
from app.service.filter import filter_movies
from app.service.filter import FilterRequest
from ..embeddings.service import embed_query
from ..retrieval.retrieval_service import retrieve_movies, retrieve_movies_multi
from ..recommender.ranking.ranking_service import rank_movies

def recommend_pipeline(state: AgentState):

    query = state.query
    filters = state.filters
    top_k = state.top_k
    user_mode = state.user_mode
    expanded_queries = state.expanded_queries

    print("\n\n FILTROS (en service/recommendation_pipeline.py): ", filters)
    print("USER MODE (en service/recommendation_pipeline.py): ", user_mode)
    print("EXPANDED QUERIES: ", expanded_queries)

    conn =  get_connection()

    try:
        # 1. Apply filters and expanded queries
        allowed_ids = None
        if filters:
            allowed_ids = filter_movies(
                FilterRequest(
                    genres=filters.get("genres", []),
                    min_rating=filters.get("min_rating", 0.0),
                    year_from=filters.get("year_from", 1900),
                    year_to=filters.get("year_to", 2100)),
                    conn
            )
            print("NUMERO DE ALLOWED IDS DESPUÉS DE FILTRAR:", len(allowed_ids))

        if expanded_queries:
            # Original queries + new queries created by the LLM
            all_queries = [query] + expanded_queries
            candidates = retrieve_movies_multi(
                queries=all_queries,
                top_k=top_k,
                allowed_ids=allowed_ids
            )

        else:
            # 2. Encoding the query into an embedding
            query_embedding = embed_query(query)

            # 3. Retrieval (candidates)
            candidates = retrieve_movies(
                query_embedding=query_embedding,
                top_k=top_k,
                allowed_ids=allowed_ids
            )

        # 4. Ranking (final decision)
        ranked_movies = rank_movies(
            candidates=candidates,
            user_filters=filters,
            user_mode=user_mode)
                
        # Return the top-K final movies, only the title
        return (
            [movie[1] for movie in ranked_movies[:top_k]],
            [movie[0] for movie in ranked_movies[:top_k]]
        )
    
    finally:
        conn.close()
