from pydantic import BaseModel
from typing import List, Literal


class SceneSpec(BaseModel):
    scene_id: str
    goal: str
    visual_elements: List[str]
    estimated_duration_sec: int
    narrative_intent: str


class ScriptPlan(BaseModel):
    topic: str
    total_duration_sec: int
    scenes: List[SceneSpec]
