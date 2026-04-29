import requests

def get_embedding(text: str):

    """
    Make the call to the model
    """

    response = requests.post(
        "http://ollama:11434/api/embeddings",
        #"http://localhost:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    response.raise_for_status()  # 👈 clave para debug real

    data = response.json()

    if "embedding" not in data:
        raise ValueError(f"Ollama error: {data}")

    return data["embedding"]