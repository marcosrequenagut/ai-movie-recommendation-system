from app.agent.tools import recommend_tool, explain_tool
from app.agent.router_prompt import decide_action

def run_agent(user_input):

    decision = decide_action(user_input)

    action = decision["action"]
    print("\n\n\n\n\n\n\n\nACTION:", action,"\n\n\n\n\n\n\n\n")


    if action == "recommend":
        results = recommend_tool(decision["query"])
        print("Recommend results: ", results)
        return {"type": "recommendation", "data": results}
    
    if action == "explain":
        results = explain_tool(
            query = decision["query"],
            movie = decision["movie"],
            metadata = {}
        )

        return {"explanation": results}

    if action == "clarify":
        return {"response": "I’m not sure I understood your request. Do you want a movie recommendation or an explanation about a movie? Please rephrase your question."}