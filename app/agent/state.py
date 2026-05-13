from pydantic import BaseModel, Field
from typing import List, Optional, Any, Annotated

def accumulate_history(existing: list, new: list) -> list:
    """Reducer: increase the historical data between API calls"""

    return(existing or []) + (new or [])

# Create a state model to hold the current state of the agent
# Standard structure for ALL the nodes
class AgentState(BaseModel):
    """
    This class is what the graph uses internally while executing (LangGraph internal memory)"""
    # Inputs of the user
    query: str
    filters: Optional[dict] = None
    top_k: int = 5
    user_mode: Optional[str] = "smart"

    # Results of the actual call
    movies: List[str] = Field(default_factory=list) # Create a new empty list every time you instantiate the class. Each object gets its own independent list
    explanation: Optional[str] = None
    message: Optional[str] = None

    # Metadata
    metadata: Optional[Any] = None
    action: Optional[str] = None

    # Clarify control
    clarify_count:  int = 0

    # Query expansion
    expanded_queries: List[str] = Field(default_factory=list)

    # Conversational memory
    conversation_history: Annotated[List[dict], accumulate_history] = Field(default_factory=list)

