from pydantic import BaseModel
from typing import Optional

class AgentRequest(BaseModel):
    """This class is what the user sends to the system (API Layer)"""
    query: str
    top_k: Optional[int] = 5
    filters: Optional[dict] = None
    user_mode: Optional[str] = "smart"