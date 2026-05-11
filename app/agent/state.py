from pydantic import BaseModel, Field
from typing import List, Optional, Any

# Create a state model to hold the current state of the agent
# Standard structure for ALL the nodes
class AgentState(BaseModel):
    """
    This class is what the graph uses internally while executing (LangGraph internal memory)"""
    query: str
    filters: Optional[dict] = None
    top_k: int = 5
    metadata: Optional[Any] = None
    action: Optional[str] = None
    movies: List[str] = Field(default_factory=list) # Create a new empty list every time you instantiate the class. Each object gets its own independent list
    user_mode: Optional[str] = "smart"
    explanation: Optional[str] = None
    message: Optional[str] = None
    year_from: Optional[int] = 1900
    year_to: Optional[int] = 2100
    clarify_count:  int = 0
    semantic_flag: bool = False # Necessary when the clarify option is selected. It prevents to reexecute the semantic_filter_node.