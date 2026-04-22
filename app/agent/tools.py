from app.recommender.recommender import get_recommended_movies
from app.service.explainer import generate_explanation  

def recommend_tool(query):
    return get_recommended_movies(query)

def explain_tool(query, movie, metadata):
    return generate_explanation(query, movie, metadata)