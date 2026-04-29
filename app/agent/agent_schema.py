from pydantic import BaseModel
from typing import Optional

class AgentRequest(BaseModel):
    message: str
    top_k: Optional[int] = 5
    genres: Optional[list[str]] = None
    user_mode: Optional[str] = "smart"