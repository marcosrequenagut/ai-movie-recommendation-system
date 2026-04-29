from app.agent.state import AgentState
from app.agent.router_node import router_node
from app.agent.nodes import recommend_node, explain_node

def run_graph(state: AgentState):
    
    state = router_node(state)

    if state.action == "recommend":
        return recommend_node(state)
    
    elif state.action == "explain":
        return explain_node(state)
    
    else:
        return {"error": "Invalid action. Supported actions are 'recommend' and 'explain'."}