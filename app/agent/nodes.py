from app.agent.state import AgentState
from app.service.explainer import generate_explanation
from app.service.recommendation_pipeline import recommend_pipeline
from app.agent.router_prompt import call_llm

from typing import Dict, Any
import json


def recommend_node(state: AgentState) -> Dict[str, Any]:
    ranked_movies, movies_ids = recommend_pipeline(state)
    print("\n=== RECOMMEND NODE ===")
    print("\nMOVIES IDS: ", movies_ids)
    
    print(f"Recommendation result: {ranked_movies}")

    return {
        "movies": ranked_movies,
        "recommended_ids": movies_ids
        }

def explain_node(state: AgentState) -> Dict[str, Any]:
    print("\n=== ENTER EXPLAIN ===")
    print("FULL STATE:")
    print(state.model_dump())

    print("RECOMMENDED IDS:")
    print(state.recommended_ids)
    explanation = generate_explanation(state)
    return {
        "explanation": explanation
        }

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
    You are a query disambiguation system for a movie assistant.

    The system can only handle TWO actions:

    1. RECOMMEND_MOVIES
    - The user wants movie suggestions
    - Example intent: "I want movies like X", "recommend me films", "similar to..."

    2. EXPLAIN_MOVIE
    - The user wants explanation about a specific movie
    - Example intent: "why do you recommend Interestellar?"

    ---

    USER INPUT:
    {state.raw_query}

    ---

    TASK:
    You MUST:
    1. Decide ONLY ONE intent: RECOMMEND_MOVIES or EXPLAIN_MOVIE
    2. Rewrite the query accordingly
    3. Remove all ambiguity
    4. Do NOT include both options
    5. Do NOT use words like "or", "either", "maybe"

    ---

    OUTPUT FORMAT (STRICT):

    INTENT: <RECOMMEND_MOVIES or EXPLAIN_MOVIE>
    QUERY: <clear rewritten query>

    ---

    EXAMPLES:

    User: "movies like Interstellar or explain Interstellar"
    Output:
    INTENT: RECOMMEND_MOVIES
    QUERY: Recommend movies similar to Interstellar

    User: "what is Interstellar about"
    Output:
    INTENT: EXPLAIN_MOVIE
    QUERY: Explain the plot of Interstellar

    ---

    Now process the user input.
    """
    
    new_query = call_llm(new_prompt)
    
    print("\nOLD QUERY: ", state.query)
    print("\nIMPROVE_QUERY: ", new_query)
    
    return {
        "query": new_query,
        "action": "clarify",
        "clarify_count": clarify_count}

def format_output_node(state: AgentState) -> Dict[str, Any]:
    print("\n=== FORMAT OUTPUT ===")
    # Recover current history (from checkpointer or empty if first call)
    current_history = state.conversation_history or []
    recommended_ids = state.recommended_ids or []

    print("\nRECOMMENDED IDS IN FORMAT OUTPUT NODES: ", recommended_ids)

    # Create the message of the LLM in a natural language
    if state.movies:
        assistant_content = f"I recommended the following movies: {', '.join(state.movies)}"
    elif state.message:
        assistant_content = state.message
    elif state.explanation:
        assistant_content = state.explanation
    else:
        assistant_content = "No results found."

    new_message = [
        {"role": "user", "content": state.raw_query},
        {"role": "assistant", "content": assistant_content}
    ]

    result = {
        "query": state.query,
        "action": state.action,
        "movies": state.movies,
        "explanation": getattr(state, "explanation", None), # If the attribute doesn't exist, return None
        "message": getattr(state, "message", None),  # If the attribute doesn't exist, return None
        "top_k": state.top_k,
        "conversation_history": new_message,
        "recommended_ids": recommended_ids
    }

    print("\nRESULT IN THE OUTPUT NODE: ", result)

    return result

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
    
    # Build conversation context
    if state.conversation_history:
        history_text = "\n".join([
            f"USER: {msg['content']}"
            for msg in state.conversation_history
            if msg.get("role") == "user"
        ])
        context_block = f"""
        ## CONVERSATION HISTORY - Previous user requests (use this to understand genre evolution):
        {history_text}

        ## CURRENT USER REQUEST:
        {state.query}
        """
    else:
        context_block = f"""
            ## USER REQUEST:
            {state.query}
        """

    print("\nCONTECT BLOCK: ", context_block)

    prompt = f"""You are a movie genre extraction system. Your task is to determine which genres should be active RIGHT NOW based on the full conversation context and the current user request.

            ## STRICT RULES:
            1. **DO NOT INVENT GENRES** - Only use genres from the official list: {all_possible_genres}
            2. **ONLY RETURN JSON** - No explanations, no comments
            3. **READ THE FULL CONTEXT** - Consider what the user wants now, including additions and removals
            4. **HANDLE MODIFICATIONS** - If the user says "remove X" or "without X", exclude that genre
            5. **HANDLE ADDITIONS** - If the user says "add X" or "also X", include previous genres plus new ones

            ## OFFICIAL VALID GENRES LIST:
            {all_possible_genres}

            ## RECOGNIZED SYNONYMS AND VARIANTS:
            - "Sci-Fi", "sci fi", "science fiction" → "Science Fiction"
            - "scary", "terror" → "Horror"
            - "romantic", "love" → "Romance"
            - "funny", "humor" → "Comedy"
            - "dramatic" → "Drama"
            - "suspense", "suspenseful" → "Thriller"
            - "animated", "cartoon" → "Animation"
            - "kids", "children" → "Family"
            - "gangster", "mafia" → "Crime"
            - "military", "battle" → "War"
            - "cowboy" → "Western"
            - "magical", "magic" → "Fantasy"
            - "detective", "whodunit" → "Mystery"
            - "historical" → "History"
            - "musical", "singing" → "Music"

            ## RESPONSE FORMAT:
            {{"detected_genres": ["Genre1", "Genre2"]}}

            ## EXAMPLES WITH CONTEXT:

            History: USER: emotional adventure movies / ASSISTANT: recommended...
            Current: "remove adventure and add horror"
            Response: {{"detected_genres": ["Drama", "Horror"]}}

            History: USER: sci-fi movies / ASSISTANT: recommended...
            Current: "and also horror"
            Response: {{"detected_genres": ["Science Fiction", "Horror"]}}

            History: (empty)
            Current: "funny animated movies for kids"
            Response: {{"detected_genres": ["Comedy", "Animation", "Family"]}}

            {context_block}

            Remember: ONLY RESPOND WITH THE JSON. NOTHING ELSE."""

    detected_genres_dict = call_llm(prompt=prompt)
    print(f"\nGENRES LIST UPDATED AFTER THE PROMPT: {detected_genres_dict}")

    # The prompt is returning a string with json strcuture
    if isinstance(detected_genres_dict, str):
        detected_genres_dict = json.loads(detected_genres_dict)

    
    detected_genres_list = detected_genres_dict["detected_genres"] or []

    print(f"\nGENRES LIST DETECTED BY THE LLM: {detected_genres_list}")

    # Make sure that only possible generes are in the list
    valid_genres = [g for g in detected_genres_list if g in all_possible_genres]
    detected_genres_list = valid_genres

    # Obtain the actual filters
    current_filters = state.filters or {}

    # Get a copy of the  original filters to not override them
    copy_current_filters = current_filters.copy()

    # Make sure that only possible generes introduced by the user are in the list
    user_genres = copy_current_filters.get("genres") or []
    valid_user_genres = [g for g in user_genres if g in all_possible_genres]

    # Final list of genres validated introduced by the user
    copy_current_filters["genres"] = valid_user_genres

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

def contextualize_query_node(state: AgentState) -> Dict[str, Any]:
    """
    This node takes the conversation_history, using all the user's queries, and
    creates a summarized query representing everything the user has requested.
    If conversation_history contains more than one query, then raw_query and query
    are different; otherwise, they are the same.
    """

    print("\nCONVERSATION HISTORY: ", state.conversation_history)
    
    # Extract all the queries of the user
    if state.conversation_history:
        past_queries = [
            msg['content'] for msg in state.conversation_history if msg.get("role") == "user"
        ]

        # Build history iwth past queries + current raw query
        all_queries = past_queries + [state.raw_query]

        history_query = "\n".join([
            f"QUERY {i}: {q}" for i, q in enumerate(all_queries, start=1)
        ])
        
    else:
        all_queries = [state.raw_query]
        # First call, no history
        history_query = f"QUERY 1: {all_queries[0]}"

    print(f"\nHISTORY QUERY: {history_query}")

    prompt = f"""
        You are a conversational query rewriting system for a movie recommendation AI.

        Your task is to analyze the full conversation history and generate a single final query that represents the user's CURRENT intent.

        The conversation history is ordered from oldest query to newest query.

        IMPORTANT RULES:

        1. Prioritize the MOST RECENT user requests over older ones.
        2. If the user changes preferences, the newest preference replaces the old one.
        3. Preserve compatible preferences from older queries when they are not contradicted.
        4. Remove outdated or conflicting preferences.
        5. Generate ONLY one final rewritten query.
        6. Do not explain your reasoning.
        7. Do not return JSON.
        8. Return ONLY the rewritten query as plain text.
        9. The rewritten query must be optimized for semantic search and embeddings.
        10. Make the final intent explicit and descriptive.

        EXAMPLE:

        Conversation:
        QUERY 1: I want emotional horror movies
        QUERY 2: Actually replace horror with action

        Output:
        emotional action movies

        EXAMPLE:

        Conversation:
        QUERY 1: Recommend emotional sci-fi movies
        QUERY 2: I want something scarier
        QUERY 3: I changed my mind, I want something realistic and not sci-fi

        Output:
        realistic emotional thriller and drama movies without sci-fi elements

        Now rewrite the following conversation into a single final query representing the user's latest intent:

        {history_query}
    """

    # If there is no previous history, just copy the actual query
    if len(all_queries) == 1:
        contextual_query = state.raw_query
    else:
        contextual_query = call_llm(prompt=prompt)

    print(f"\nNEW CONTEXTUAL QUERY: {contextual_query}")
    print(f"RAW QUERY: {state.raw_query}")

    return {
        "query": contextual_query
        }


def intent_node(state: AgentState) -> Dict[str, Any]:
    """
    Lightweight intent classifier that detects ONLY if the user wants an explanation.
    Uses raw_query without any conversation history to avoid contamination.
    If explain → goes directly to explain_node skipping contextualization.
    If other  → continues to contextualize_query → semantic_filter → router.
    """

    prompt = f"""You are a strict intent classifier for a movie recommendation system.

    ## YOUR ONLY TASK:
    Decide if the user wants an EXPLANATION about a specific movie or recommendation.

    ## CLASSIFY AS "explain" IF:
    - The user asks why a movie was recommended
    - The user asks for details or information about a specific movie
    - The user asks to elaborate on a previous recommendation
    - The user mentions a specific movie title and asks something about it

    ## CLASSIFY AS "other" IF:
    - The user asks for movie recommendations (new or refined)
    - The user wants to add, remove or change genres/preferences
    - The user asks something unrelated to a specific movie explanation

    ## STRICT RULES:
    1. ONLY return JSON, no extra text
    2. Analyze ONLY the current message, ignore any context
    3. When in doubt, classify as "other"

    ## RESPONSE FORMAT:
    {{"intent": "explain"}} or {{"intent": "other"}}

    ## EXAMPLES:

    User: "why did you recommend Beetlejuice?"
    Response: {{"intent": "explain"}}

    User: "tell me more about Interstellar"
    Response: {{"intent": "explain"}}

    User: "what makes Her a good pick?"
    Response: {{"intent": "explain"}}

    User: "explain that last recommendation"
    Response: {{"intent": "explain"}}

    User: "add horror to my recommendations"
    Response: {{"intent": "other"}}

    User: "recommend me sci-fi movies"
    Response: {{"intent": "other"}}

    User: "only from the 90s"
    Response: {{"intent": "other"}}

    User: "why not something more recent?"
    Response: {{"intent": "other"}}

    ## USER MESSAGE:
    "{state.raw_query}"

    Remember: ONLY return the JSON. Nothing else."""

    raw_llm_response = call_llm(prompt=prompt)

    # Parse the response
    if isinstance(raw_llm_response, str):
        try:
            parsed = json.loads(raw_llm_response)
        except Exception:
            # Fallback to other if parsing fails
            print(f"\n\n\nFAILED INTENT_NODE PARSE, RETURNING 'OTHER' AS THE DEFAULT INTENTION")
            parsed = {"intent":"other"}

    intent = parsed.get("intent", "other")

    print(f"\nINTENT DETECTED IN THE INTENT_NODE: {intent}")

    # Map intent to the action
    action = "explain" if intent == "explain" else None

    return {
        "action": action
    }