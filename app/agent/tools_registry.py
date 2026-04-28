from app.service.explainer import generate_explanation
from app.service.recommendation_pipeline import recommend_pipeline

TOOLS = {
    "recommend": recommend_pipeline,
    "explain": generate_explanation
}