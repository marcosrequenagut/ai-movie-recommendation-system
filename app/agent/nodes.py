from app.agent.state import AgentState
from app.service.explainer import generate_explanation
from app.service.recommendation_pipeline import recommend_pipeline
from app.agent.router_prompt import call_llm

from typing import Dict, Any
import json


def recommend_node(state: AgentState) -> Dict[str, Any]:
    ranked_movies = recommend_pipeline(state)
    
    print(f"Recommendation result: {ranked_movies}")
    print(f"state before returning from recommend_node: {state}")

    return {"movies": ranked_movies} # It updates the "movies" key of the old state

def explain_node(state: AgentState) -> Dict[str, Any]:
    explanation = generate_explanation(state)
    return {"explanation": explanation}

def clarify_node(state: AgentState) -> Dict[str, Any]:
    """This function, rewrites the user query into a cleare version for the router.
    It does it 3 times, if the router continue chosing the "clarify" option, the node
    sends a message to the user to rewrite by itself the query."""

    clarify_count = state.clarify_count + 1

    print("\n\n\ITERATIONS: ", clarify_count)

    # Stop condition
    if clarify_count >=3:
        return {
            "action": "final_clarify",
            "message":"I didn't fully understand. Please rephrase your request for movie recommendations or explanations.",
            "clarify_count": clarify_count
        }
    
    # New prompt to rephrase the query
    new_prompt = f"""
        The user asked something unclear: {state.query}

        This system only:
            - recommends movies
            - explain recommended movies
        
        Rewrite the user's request into a clearer movie-related query.
        Rephrase user's request for movie recommendation or explanations purposes.
        """
    
    new_query = call_llm(new_prompt)
    
    print("\nOLD QUERY: ", state.query)
    print("\nIMPROVE_QUERY: ", new_query)
    
    return {
        "query": new_query,
        "action": "clarify",
        "clarify_count": clarify_count}

def format_output_node(state: AgentState) -> Dict[str, Any]:
    
    return {
        "query": state.query,
        "action": state.action,
        "movies": state.movies,
        "explanation": getattr(state, "explanation", None), # If the attribute doesn't exist, return None
        "message": getattr(state, "message", None),  # If the attribute doesn't exist, return None
        "top_k": state.top_k
    }

def final_clarify_node(state: AgentState) -> Dict[str, Any]:
    return {
        "message": state.message,
        "action": "end"
    }

def semantic_filter_node(state: AgentState) -> AgentState:
    """The objective of this funtion is trying to detect film genres into the input 
    of the user. This function will call the LLM and will try to extract some genres 
    information. Those genres will be restricted to those who appear in the 
    PostGrees DB."""

    all_possible_genres = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary',
        'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction',
        'TV Movie', 'Thriller', 'War', 'Western']
    
    prompt = f"""You are a movie genre extraction system. Your ONLY task is to identify genres in the user's query and map them to the official genre list provided.

        ## STRICT RULES (YOU MUST FOLLOW THEM TO THE LETTER):

        1. **DO NOT INVENT GENRES** - If a genre is not in the official list, DO NOT include it.
        2. **ONLY RETURN JSON** - Your response MUST be a valid JSON object only.
        3. **NO EXTRA TEXT** - No explanations, no comments, only JSON.
        4. **NO EXTRA CAPITALIZATION** - Use EXACTLY the same name as in the official list.

        ## OFFICIAL VALID GENRES LIST:
        {all_possible_genres}

        ## RECOGNIZED SYNONYMS AND VARIANTS:

        - "Sci-Fi", "Sci Fi", "SciFi", "sci fi", "science fiction" → "Science Fiction"
        - "Action" → "Action" (any form of action)
        - "Comedy", "funny", "humor" → "Comedy"
        - "Horror", "scary", "terror" → "Horror"
        - "Romance", "romantic", "love" → "Romance"
        - "Adventure", "adventurous" → "Adventure"
        - "Animation", "animated", "cartoon" → "Animation"
        - "Crime", "criminal", "gangster", "mafia" → "Crime"
        - "Documentary", "doc", "real story" → "Documentary"
        - "Drama", "dramatic" → "Drama"
        - "Fantasy", "magical", "magic" → "Fantasy"
        - "History", "historical" → "History"
        - "Music", "musical", "singing" → "Music"
        - "Mystery", "detective", "whodunit" → "Mystery"
        - "Thriller", "suspense", "suspenseful" → "Thriller"
        - "War", "military", "battle" → "War"
        - "Western", "cowboy" → "Western"
        - "Family", "kids", "children" → "Family"
        - "TV Movie", "made for TV" → "TV Movie"

        ## RESPONSE FORMAT (ONLY THIS, NOTHING ELSE):

        These are the only 3 possible cases:

        Case 1: You find one or more genres
        {{"detected_genres": ["Science Fiction", "Action"]}}

        Case 2: You find NO genres
        {{"detected_genres": []}}

        Case 3: User mentions a genre NOT in the official list
        {{"detected_genres": []}}  # DO NOT invent, just empty array

        ## EXAMPLES:

        User: "Recommend me a Sci-Fi movie"
        Response: {{"detected_genres": ["Science Fiction"]}}

        User: "I want a romantic comedy with action"
        Response: {{"detected_genres": ["Romance", "Comedy", "Action"]}}

        User: "Show me a scary movie about space"
        Response: {{"detected_genres": ["Horror", "Science Fiction"]}}

        User: "Give me a good film"
        Response: {{"detected_genres": []}}

        User: "Something like Star Wars"
        Response: {{"detected_genres": ["Science Fiction"]}}

        User: "A crime drama with a gangster"
        Response: {{"detected_genres": ["Crime", "Drama"]}}

        User: "Recommend a fantasy movie with dragons"
        Response: {{"detected_genres": ["Fantasy"]}}

        User: "I want a funny animated film for kids"
        Response: {{"detected_genres": ["Comedy", "Animation", "Family"]}}

        User: "A western cowboy movie"
        Response: {{"detected_genres": ["Western"]}}

        User: "A mysterious thriller with suspense"
        Response: {{"detected_genres": ["Mystery", "Thriller"]}}

        User: "Show me a musical with singing"
        Response: {{"detected_genres": ["Music"]}}

        User: "A historical war film"
        Response: {{"detected_genres": ["History", "War"]}}

        ## NOW, PROCESS THE FOLLOWING USER QUERY:

        User query: {state.query}

        Remember: ONLY RESPOND WITH THE JSON. NOTHING ELSE."""

    detected_genres_dict = call_llm(prompt=prompt)
    print(f"\nGENRES LIST UPDATED AFTER THE PROMPT: {detected_genres_dict}")

    # The prompt is returning a string with json strcuture
    if isinstance(detected_genres_dict, str):
        detected_genres_dict = json.loads(detected_genres_dict)

    
    detected_genres_list = detected_genres_dict["detected_genres"] or []

    print(f"\nGENRES LIST DETECTED BY THE LLM: {detected_genres_list}")

    # Obtain the actual filters
    current_filters = state.filters or {}

    # Get a copy of the  original filters to not override them
    copy_current_filters = current_filters.copy()

    # Obtain the genres list
    current_genres = copy_current_filters.get("genres") or []

    print(f"\nGENRES INTRODUCED BY THE USER: {current_genres}")

    # Combine new and old genres list without duplicates
    updated_genres_list = list(set(current_genres + detected_genres_list))

    # Update the "genres" filter
    copy_current_filters["genres"] = updated_genres_list

    print(f"\nGENRES LLM + GENRES USER: {copy_current_filters}")


    return {
        "filters": copy_current_filters
        }

def query_expansion_node(state: AgentState) -> Dict[str, Any]:
    """
    This function expands the user query into 3 semantic variants using the LLM.
    This improve vector search recall by covering more semantic ground.
    Only runs when action == "recommmend
    """    
    prompt = f"""You are a movie search query expansion system. Your task is to rewrite the user's query into 3 different semantic variants to improve movie search results.

        ## STRICT RULES:
        1. ONLY RETURN JSON - no explanations, no comments
        2. Each variant must be semantically different, not just paraphrasing
        3. Keep variants focused on movies
        4. Use different vocabulary and angles for each variant

        ## RESPONSE FORMAT (ONLY THIS):
        {{"expanded_queries": ["variant 1", "variant 2", "variant 3"]}}

        ## EXAMPLES:

        User: "emotional sci-fi movies"
        Response: {{"expanded_queries": ["philosophical science fiction with human drama", "thought-provoking futuristic films about humanity", "existential space stories with deep emotional themes"]}}

        User: "funny movies for a Friday night"
        Response: {{"expanded_queries": ["light-hearted comedy films for entertainment", "hilarious movies with happy endings", "fun and easy-going films to watch with friends"]}}

        User: "scary horror movies"
        Response: {{"expanded_queries": ["terrifying psychological horror films", "suspenseful thriller with frightening atmosphere", "dark and disturbing horror with intense scenes"]}}

        ## NOW PROCESS THIS QUERY:
        User: "{state.query}"

        Remember: ONLY RESPOND WITH THE JSON. NOTHING ELSE.
    """

    raw_response = call_llm(prompt)

    print(f"\nQUERY EXPANSION RAW RESPONSE: {raw_response}")

    # Parse the response if it is a string
    if isinstance(raw_response, str):
        parsed = json.loads(raw_response)
    else:
        parsed = raw_response

    expanded = parsed.get("expanded_queries", [])

    print(f"\nEXPANDED QUERIES: {expanded}")
    
    return {
        "expanded_queries": expanded
    }