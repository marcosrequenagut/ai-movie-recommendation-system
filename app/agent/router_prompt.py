from app.agent.router_schema import RouterOutput

import requests
import json
import re

#OLLAMA_URL = "http://ollama:11434/api/generate"
OLLAMA_URL = "http://localhost:11434/api/generate"

def parse_router_output(raw_text: str) -> RouterOutput:

    try:
        json_data = extract_json(raw_text)
        data = json.loads(json_data)
        return RouterOutput(**data)
    
    except Exception:
        return RouterOutput(
            action="clarify",
            query="",
            movie="")
    
def extract_json(raw_text: str) -> str:
    """
    This function extracts the JSON object from the raw
    text created by de LLM model
    """
    match = re.search(r"\{.*\}", raw_text, re.DOTALL)

    if not match:
        raise ValueError("No JSON object found in the text")
    
    return match.group(0)

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
