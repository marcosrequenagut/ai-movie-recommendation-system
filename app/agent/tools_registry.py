from app.service.explainer import generate_explanation
from app.service.recommendation_pipeline import recommend_pipeline

def recommend_tool(input: dict):
    return recommend_pipeline(
        query=input.get("query"),
        filters=input.get("filters"),
        top_k=input.get("top_k", 5)
    )

def explain_tool(input: dict):
    return generate_explanation(
        query=input.get("query"),
        movie=input.get("movie"),
        metadata=input.get("metadata")
    )

TOOLS = {
    "recommend": recommend_tool,
    "explain": explain_tool
}