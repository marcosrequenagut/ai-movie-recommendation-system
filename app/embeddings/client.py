import requests

def get_embedding(text: str):

    """
    Make the call to the model
    """

    response = requests.post(
        "http://ollama:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    return response.json()["embedding"]