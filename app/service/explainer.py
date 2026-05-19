import requests

from app.agent.state import AgentState

#OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_URL = "http://ollama:11434/api/generate"

def generate_explanation(agent_state: AgentState) -> str:
    
    raw_query = agent_state.raw_query
    conversation_history = agent_state.conversation_history or []

    # Build conversation context — only user queries and assistant recommendations
    history_text = "\n".join([
        f"{msg['role'].upper()}: {msg['content']}"
        for msg in conversation_history
    ])

    prompt = f"""You are a movie recommendation assistant.

    The user is asking for an explanation about a previous movie recommendation.

    ## CONVERSATION HISTORY:
    {history_text}

    ## CURRENT USER QUESTION:
    {raw_query}

    ## YOUR TASK:
    1. Identify which movie the user is asking about from the conversation history.
    2. Find the recommendation context — what the user was looking for when that movie was recommended.
    3. Write a clear and natural explanation of why that movie was a good match.

    ## INSTRUCTIONS:
    - Write 2-4 sentences maximum.
    - Explicitly connect the user's original preferences with the movie's characteristics.
    - Mention specific elements: genre, themes, mood, tone, or style.
    - Do NOT mention embeddings, algorithms, vectors, or any system logic.
    - Do NOT invent information about the movie that is not inferable from the conversation.
    - If you cannot identify which movie the user is asking about, ask for clarification.

    ## OUTPUT FORMAT:
    A single natural language paragraph. No lists, no headers, no JSON.
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    data = response.json()
    generated_explanation = data.get("response", "")
    print(f"\nEXPLANATION GENERATED: {generated_explanation}")

    return generated_explanation