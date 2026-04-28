from app.agent.tools import recommend_tool, explain_tool
from app.agent.router_prompt import decide_action
from app.agent.tools_registry import TOOLS
from app.service.explainer import generate_explanation
from app.service.recommendation_pipeline import recommend_pipeline

def agent(user_input, filters=None, top_k=5):

    decision = decide_action(user_input)

    action = decision["action"]
    query = decision["query"]
    movie = decision.get("movie", "")
    print("\n\n\n\n\n\n\n\nACTION:", action,"\n\n\n\n\n\n\n\n")

    # 1. fallback
    if action not in TOOLS:
        return {
            "error": "I'm not sure I understood your request. Do you want a movie recommendation or an explanation about a movie? Please rephrase your question."
        }
    
    # 2. Tool selection
    tool = TOOLS[action]

    # 3. Execution layer
    if action == "recommend":
        return tool(query, filters, top_k)
    
    elif tool == "explain":
        return tool(
            query = query,
            movie = movie,
            metadata = None
        )
