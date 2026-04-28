from ..db.connection import get_connection
from ..embeddings.service import embed_query
from ..retrieval.retrieval_service import retrieve_movies


def get_recommended_movies(query, top_k=5, allowed_ids=None):

    # 1. Encoding
    query_embedding = embed_query(query)

    # 2. Retrieval (DB + repository)
    results = retrieve_movies(
        embedding=query_embedding,
        allowed_ids=allowed_ids,
        top_k=top_k
    )

    return results