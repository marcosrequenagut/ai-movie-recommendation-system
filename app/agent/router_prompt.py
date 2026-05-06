from app.agent.router_schema import RouterOutput

import requests
import json
import re

OLLAMA_URL = "http://ollama:11434/api/generate"
#OLLAMA_URL = "http://localhost:11434/api/generate"

def parse_router_output(raw_text: str) -> RouterOutput:
    """Create a parse logic for the decide action output"""

    try:
        json_data = extract_json(raw_text)
        data = json.loads(json_data)
        return RouterOutput(**data)
    
    except Exception as e:
        print(f"Router error: {e}")

        return RouterOutput(
            action="clarify")
    
def extract_json(raw_text: str) -> str:
    """
    Extracts the first valid JSON object from a messy LLM output.
    """

    # Remove markdown code fences if present
    cleaned = re.sub(r"```json|```", "", raw_text).strip()

    # Try direct parse first (fast path)
    try:
        json.loads(cleaned)
        return cleaned
    except Exception:
        pass

    # Fallback: regex extraction
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)

    if not match:
        raise ValueError("No JSON object found in LLM output")

    return match.group(0)

def decide_action(user_input: str) -> RouterOutput:

    """This function decides which action has to take the Agent by creating a json where the action is indicated."""

    prompt = f"""
    You are a strict JSON router.

    You MUST choose ONE action: "recommend", "explain", or "clarify".

    Decision rules (apply in order):

    1. If the user asks for movie recommendations → action = "recommend"
    2. If the user mentions a specific movie → action = "explain"
    3. Only if the request is too vague → action = "clarify"

    IMPORTANT:
    - DO NOT overuse "clarify"
    - Your response must be valid JSON.
    - No markdown. No extra text.
    
    Output format:

    {{
    "action": "<recommend|explain|clarify>"
    }}

    EXAMPLES:

    User: "Recommend a sci-fi movie"
    Output: {{"action": "recommend"}}

    User: "What is Interstellar about?"
    Output: {{"action": "explain"}}

    User: "I want something good"
    Output: {{"action": "clarify"}} 


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
