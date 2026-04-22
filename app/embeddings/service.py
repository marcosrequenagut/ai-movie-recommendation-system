from .client import get_embedding

def embed_query(query: str):
    # preprocessing
    query = query.lower().strip()

    # logging / metrics
    print("Embedding query:", query)

    return get_embedding(query)