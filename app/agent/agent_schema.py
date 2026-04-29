from pydantic import BaseModel
from typing import Optional

class AgentRequest(BaseModel):
    message: str
    top_k: Optional[int] = 5