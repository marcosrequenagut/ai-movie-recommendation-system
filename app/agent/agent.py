from app.agent.execute_graph import execute_graph
from app.agent.router_prompt import decide_action
from app.agent.state import AgentState
from app.agent.tools_registry import TOOLS

def agent(user_input, filters=None, top_k=5):

    decision = decide_action(user_input)

    state = AgentState(
        query=decision.query,
        movie=decision.movie,
        filters=filters,
        top_k=top_k,
        metadata=None
    )

    return execute_graph(state, decision.action)