from app.agent.router_schema import RouterOutput
from typing import Any

import requests
import json
import re

OLLAMA_URL = "http://ollama:11434/api/generate"
#OLLAMA_URL = "http://localhost:11434/api/generate"

def parse_router_output(raw_text: Any) -> RouterOutput:
    """Create a parse logic for the decide action output"""

    # If it receives a dict, it extracts the response field and the decide_action value.
    if isinstance(raw_text, dict):
        # Raw text is a dictionary. Response is a dictionary with a key as a form of string dictionary: {"response": '{"action": "recommend"}'}
        raw = raw_text["response"]

        # Transform the value string in a dictionary
        dict_raw = json.loads(raw)

        # Extract the string decide_action: "clarify", "recommend", "explain"
        decide_action = dict_raw["action"]
        return RouterOutput(**dict_raw)

    try:
        json_data = extract_json(raw_text)
        data = json.loads(json_data)
        return RouterOutput(**data)
    
    except Exception as e:
        print(f"Router error: {e}")

        return RouterOutput(
            action="clarify")
    
def extract_json(raw_text: Any) -> str:
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

def call_llm(prompt: str, temperature: float = 0):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False,
            "temperature": 0
        }
    )

    return response.json()["response"]

def decide_action(user_input: str, conversation_history: list = None) -> RouterOutput:

    """
    This function decides which action has to take the Agent by creating a json where the action is indicated.
    It uses a conversation_history to upgrade the prompt.
    """

    # Build conversation contect string for the prompt
    if conversation_history:
        history_text = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in conversation_history
        ])
        content_block = f"""
        CONVERSATION HISTORY (use this to understant the context of the current request): {history_text}
        """
    else:
        content_block = ""

    prompt = f"""
    You are a strict JSON router.

    You MUST choose ONE action: "recommend", "explain", or "clarify".

    Decision rules (apply in order):

    1. If the user asks for movie recommendations → action = "recommend"
    2. If the user mentions a specific movie → action = "explain"
    3. If the user is refining or adding to a previous recommendation (e.g. "add horror", "only from the 90s", "shorter movies") → action = "recommend"
    4. Only if the request is too vague and there is no prior conversation_history → action = "clarify"

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

    If action = clarify, you MUST include:
    - message: explanation to the user
    - rewritten_query: improved version of the query (if possible)

    User: "I want something good"
    Output: {{
        "action": "clarify",
        "message": "I didn't understant your request",
        "rewritten_query: "Recommend sci-fi movies"}} 

    {content_block}

    User input:
    {user_input}
    """

    response = call_llm(prompt, temperature=0)

    print("---START----")

    # From the dictionary, take only the "action" key, where the OLLAMA model decides what action to take.
    #action_decided = json.loads(response.json()["response"])["action"]

    json_response = response
    print("\n\nRAW RESPONSE:", json_response,"\n\n")

    result = parse_router_output(json_response)
    print("PARSED RESPONSE ", result)

    print("---END----")

    return result
