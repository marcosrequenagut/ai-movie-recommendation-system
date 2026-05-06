import requests

def get_embedding(text: str):

    """
    Call Ollama embedding model (nomic-embed-text) and returns a raw vector with the embedding of the text received as an input.
    """

    response = requests.post(
        "http://ollama:11434/api/embeddings",
        #"http://localhost:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    response.raise_for_status() 

    data = response.json()

    if "embedding" not in data:
        raise ValueError(f"Ollama error: {data}")

    return data["embedding"]