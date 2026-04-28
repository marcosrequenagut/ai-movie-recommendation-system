from .client import get_embedding

def embed_query(query: str):

    # preprocessing
    query = query.lower().strip()

    return get_embedding(query)