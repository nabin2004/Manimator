from pydantic import BaseModel
from typing import Literal 

class UserIntent(BaseModel):
    topic: str 
    domain: Literal["mathematics", "physics", "AI/CS"]
    audience: Literal["school", "undergrad", "grad", "general"]
    visual_density: Literal["low", "medium", "high"]
    preferred_style: Literal["intuition", "formal", "mixed"]

