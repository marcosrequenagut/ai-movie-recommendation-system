import requests

OLLAMA_URL = "http://ollama:11434/api/generate"

def generate_explanation(query: str, movie: str, metadata: dict=None):
    prompt = f"""
    You are a movie recommendation assistant.

    Your task is to clearly explain why the movie was recommended to the user.

    User query:
    {query}

    Recommended movie:
    {movie}

    Additional info about the movie:
    {metadata}

    Instructions:
    - Write a short and natual explanation (2-4 sentences).
    - Explicity content user's query with the movie's characteristics.
    - Use ONLY the provided metadata to justify the recommendation.
    - Highlight specific similarities (e.g., genre, them, mod, actors, plot elements).
    - Do NOT mention embeddings, algorithms, or system logic.

    Output format:
    A single paragraph explanation.
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "tinyllama",
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    data = response.json()

    return data.get("response", "")