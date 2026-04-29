from app.agent.router_schema import RouterOutput

import requests
import json
import re

OLLAMA_URL = "http://ollama:11434/api/generate"
#OLLAMA_URL = "http://localhost:11434/api/generate"

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
    You are a strict JSON router.

    You MUST choose ONE action: "recommend", "explain", or "clarify".

    Decision rules (apply in order):

    1. If the user asks for movie recommendations → action = "recommend"
    2. If the user mentions a specific movie → action = "explain"
    3. Only if the request is too vague → action = "clarify"

    IMPORTANT:
    - "recommend me a dark sci-fi movie" is CLEAR → use "recommend"
    - DO NOT overuse "clarify"

    Output ONLY JSON:

    {{
    "action": "...",
    "query": "...",
    "movie": null
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

    print("\n\nRAW RESPONSE:", raw_result,"\n\n")

    result = parse_router_output(raw_result)
    print("PARSED RESPONSE ", result)

    print("---END----")

    return result
