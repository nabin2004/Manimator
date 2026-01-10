from pydantic import BaseModel
from typing import Literal, List 

class ObjectPlan(BaseModel):
    id: str 
    type: Literal["circle", "line", "dot", "axes"]
    radius: float = 0.5
    color: str = "BLUE"

class MotionPlan(BaseModel):
    target: str 
    motion: Literal["linear_move", "sinusoidal_path", "rotation"]
    params: dict 

class ScenePlan(BaseModel):
    objects: List[ObjectPlan]
    motions: List[MotionPlan]
    duration: float = 5.0