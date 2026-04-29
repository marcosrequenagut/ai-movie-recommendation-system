from app.agent.router_schema import RouterOutput

import requests
import json

#OLLAMA_URL = "http://ollama:11434/api/generate"
OLLAMA_URL = "http://localhost:11434/api/generate"

def parse_router_output(raw_text: str) -> RouterOutput:

    try:

        data = json.loads(raw_text)
        return RouterOutput(**data)
    
    except Exception:

        return RouterOutput(
            action="clarify",
            query="",
            movie="")

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

    raw_result = response.json()["response"]
    print("\n\n\n\n\n\n\n\nRAW RESPONSE:", raw_result,"\n\n\n\n\n\n\n\n")

    result = parse_router_output(raw_result)
    print("PARSED RESPONSE ", result)

    print("---END----")

    return result
