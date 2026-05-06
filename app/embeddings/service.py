from .client import get_embedding

def embed_query(query: str):
    """It preprocess the input (query) of the user"""

    # preprocessing
    query = query.lower().strip()

    return get_embedding(query)