from app.agent.state import AgentState
from app.service.explainer import generate_explanation
from app.service.recommendation_pipeline import recommend_pipeline

from typing import Dict, Any


def recommend_node(state: AgentState) -> Dict[str, Any]:
    ranked_movies = recommend_pipeline(state)
    
    print(f"Recommendation result: {ranked_movies}")
    print(f"state before returning from recommend_node: {state}")

    return {"movies": ranked_movies} # It updates the "movies" key of the old state

def explain_node(state: AgentState) -> Dict[str, Any]:
    explanation = generate_explanation(state)
    return {"explanation": explanation}

def clarify_node(state: AgentState) -> Dict[str, Any]:
    # For simplicity, we just return a placeholder response.
    # In a real implementation, this could involve asking follow-up questions to the user.
    return {"message": "Could you please clarify your request?"}

def format_output_node(state: AgentState) -> Dict[str, Any]:
    
    return {
        "query": state.query,
        "action": state.action,
        "movies": state.movies,
        "explanation": getattr(state, "explanation", None), # If the attribute doesn't exist, return None
        "message": getattr(state, "message", None),  # If the attribute doesn't exist, return None
        "top_k": state.top_k
    }