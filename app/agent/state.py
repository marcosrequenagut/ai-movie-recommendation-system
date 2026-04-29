from pydantic import BaseModel
from typing import Optional, Any

# Create a state model to hold the current state of the agent
# Standard structure for ALL the nodes
class AgentState(BaseModel):
    query: str
    movie: Optional[str] = None
    filters: Optional[Any] = None
    top_k: int = 5
    metadata: Optional[Any] = None
    action: str