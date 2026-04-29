from pydantic import BaseModel
from typing import Literal, Optional

class RouterOutput(BaseModel):
    action: Literal["recommend", "explain", "clarify"]
    query: str = ""
    movie: Optional[str] = None