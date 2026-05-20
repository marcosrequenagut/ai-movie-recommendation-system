from pydantic import BaseModel, Field
from typing import List, Optional, Any, Annotated

# Usually, in LangGraph, the state between nodes are inmutable. To change a state, we use reduce functions.
# This functions says to the system, if there is a value in the state, and another new one arrives, 
# how should i combine them? In the history case, we append them and in the ids case, we keep the 
# existing one, if the new one arrives but it is None, we keep the old state.

def accumulate_history(existing: list, new: list) -> list:
    """Reducer: increase the historical data between API calls"""

    return(existing or []) + (new or [])

def keep_previous_ids(existing: list, new: list) -> list:
    """Reducer: keep the previous movies ids of the API call if they exists"""

    return new if new else existing

# Create a state model to hold the current state of the agent
# Standard structure for ALL the nodes
class AgentState(BaseModel):
    """
    This class is what the graph uses internally while executing (LangGraph internal memory)"""
    # Inputs of the user
    query: Optional[str] = None # This is a contextual query, if a user writes some queries about the same conversation, they will be sumarize and paraphrased here
    raw_query: str # This is the query of the user when it makes an API call
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

    # Save the ids from the recommended movies to use them in the explain node
    recommended_ids:  Annotated[List[int], keep_previous_ids] = Field(default_factory=list)
