from pydantic import BaseModel
from typing import Literal

class RouterOutput(BaseModel):
    action: Literal["recommend", "explain", "clarify"]
    query: str = ""
    movie: str = ""