from app.agent.state import AgentState
from app.agent.router_prompt import decide_action
from typing import Dict, Any

def router_node(state: AgentState) -> Dict[str, Any]:
    """This node call to the decide_action. It decides the action to take: recommend, explain or clarify."""
    
    decision = decide_action(state.query)

    # Don't return the state directly, we only update the action item.
    # Internally: old_state + {"action":...}
    return {
        "action": decision.action
        }