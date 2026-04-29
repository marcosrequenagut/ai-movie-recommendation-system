from app.agent.state import AgentState
from app.service.explainer import generate_explanation
from app.service.recommendation_pipeline import recommend_pipeline


def recommend_node(state: AgentState):
    movies = recommend_pipeline(state)
    print(f"Recommendation result: {movies}")
    print(f"state before returning from recommend_node: {state}")
    return {**state.model_dump(), 
            "movies": movies}

def explain_node(state: AgentState):
    return generate_explanation(state)

def clarify_node(state: AgentState):
    # For simplicity, we just return a placeholder response.
    # In a real implementation, this could involve asking follow-up questions to the user.
    return {"message": "Could you please clarify your request?"}

def format_output_node(state: AgentState):
    
    return {
        "query": state.query,
        "action": state.action,
        "movies": getattr(state, "movies", []),
        "top_k": state.top_k
    }