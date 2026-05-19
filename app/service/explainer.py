import requests

from app.agent.state import AgentState
from app.repositories.movie_repository import search_movie_by_id
from app.db.connection import get_connection

#OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_URL = "http://ollama:11434/api/generate"

def generate_explanation(agent_state: AgentState) -> str:
    
    raw_query = agent_state.raw_query
    conversation_history = agent_state.conversation_history or []
    recommended_ids = agent_state.recommended_ids or []

    print("RECOMMENDED IDS IN EXPLAINER.PY: ", recommended_ids)

    # Fetch metadata for all recommended movies
    movies_metadata = []
    if recommended_ids:
        conn = get_connection()
        try:
            for movie_id in recommended_ids:
                result = search_movie_by_id(conn, movie_id)
                if result:
                    movies_metadata.append({
                        "title": result[1],
                        "overview": result[2],
                        "genres": result[3],
                        "release_year": result[4],
                        "vote_average": result[5],
                    })
        finally:
            conn.close()

    # Build metadata block with all recommended movies
    if movies_metadata:
        metadata_block = "## RECOMMENDED MOVIES METADATA:\n" + "\n\n".join([
            f"Title: {m['title']}\nOverview: {m['overview']}\nGenres: {m['genres']}\nYear: {m['release_year']}\nRating: {m['vote_average']}"
            for m in movies_metadata
        ])
    else:
        metadata_block = "## MOVIE METADATA: Not available."

    # Build conversation context — only user queries and assistant recommendations
    history_text = "\n".join([
        f"{msg['role'].upper()}: {msg['content']}"
        for msg in conversation_history
    ])

    print("\nMETADATA BLOCK IN EXPLAINER.PY: ", metadata_block)

    prompt = f"""You are a movie recommendation assistant.

    The user is asking why a specific movie was recommended to them.

    ## CONVERSATION HISTORY:
    {history_text}

    {metadata_block}

    ## CURRENT USER QUESTION:
    {raw_query}

    ## YOUR TASK:
    1. Identify which movie the user is asking about from their question.
    2. Find that specific movie in the RECOMMENDED MOVIES METADATA section by matching its "Title" field.
    3. Use ONLY the metadata of that specific movie to generate the explanation.
    4. Ignore the metadata of all other movies.

    ## STRICT INSTRUCTIONS:
    - Base your explanation EXCLUSIVELY on the metadata of the movie the user is asking about
    - Do NOT use your general knowledge about the movie
    - Explicitly connect the user's original preferences (from conversation history) with the movie's metadata
    - Mention specific elements: genres, overview themes, release year if relevant
    - Write 2-4 sentences maximum
    - Do NOT mention embeddings, algorithms, vectors, or system logic
    - If you cannot identify which movie the user is asking about, say "I'm not sure which movie you're referring to, could you clarify?"

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