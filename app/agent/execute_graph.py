
from app.service.explainer import generate_explanation
from app.service.recommendation_pipeline import recommend_pipeline
from app.agent.state import AgentState

def recommend_node(state: AgentState):
    return recommend_pipeline(state)

def explain_node(state: AgentState):
    return generate_explanation(state)

NODES = {
        "recommend": recommend_node,
        "explain": explain_node
    }
    
def execute_graph(state: AgentState, action: str):

    node = NODES.get(action)

    if not node:
        return {
            "error": "Invalid action. Supported actions are 'recommend' and 'explain'."
         }
    
    return node(state)