from app.agent.state import AgentState
from app.agent.router_prompt import decide_action

def router_node(state: AgentState):
    decision = decide_action(state.query)

    state.action = decision.action
    state.movie = decision.movie
    return state