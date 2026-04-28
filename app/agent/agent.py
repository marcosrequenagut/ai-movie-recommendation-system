from app.agent.tools import recommend_tool, explain_tool
from app.agent.router_prompt import decide_action
from app.service.explainer import generate_explanation
from app.service.recommendation_pipeline import recommend_pipeline

def agent(user_input, filters, top_k=5):

    decision = decide_action(user_input)

    action = decision["action"]
    query = decision["query"]
    movie = decision.get("movie", "")
    print("\n\n\n\n\n\n\n\nACTION:", action,"\n\n\n\n\n\n\n\n")


    if action == "recommend":
        return recommend_pipeline(user_input, filters, top_k)
    
    elif action == "explain":
        return generate_explanation(
            query=query,
            movie=movie,
            metadata=None)

    else:
        return {"error": "I'm not sure I understood your request. Do you want a movie recommendation or an explanation about a movie? Please rephrase your question."}