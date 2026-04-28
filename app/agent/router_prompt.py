import requests
import json

OLLAMA_URL = "http://ollama:11434/api/generate"

def decide_action(user_input):
    prompt = f"""
    You are NOT a movie recommender.

    You are ONLY a JSON router.

    DO NOT recommend movies.
    DO NOT explain anything.
    DO NOT add any text.

    If user intent is unclear or ambiguous:
    → return action = "clarify"

    If you output anything other than JSON, you FAIL.

    Return ONLY this JSON (no NOT forget the movie key, it should be always created):

    {{
    "action": "recommend | explain | clarify",
    "query": "...",
    "movie": "..."
    }}

    User input:
    {user_input}
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False,
            "temperature": 0
        }
    )

    print("---START----")
    print("\n\n\n\n\n\n\n\nRAW RESPONSE:", response.json()["response"],"\n\n\n\n\n\n\n\n")
    result = json.loads(response.json()["response"]) 
    print("This is the result of the response: ", result)
    print("---END----")

    return result