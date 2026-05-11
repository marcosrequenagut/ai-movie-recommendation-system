from pydantic import BaseModel
from typing import Literal, Optional

# The router must only decide ONE action, nothing else
class RouterOutput(BaseModel):
    action: Literal["recommend", "explain", "clarify"]

