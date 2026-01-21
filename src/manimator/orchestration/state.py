from enum import Enum
from pydantic import BaseModel
from typing import List

class SceneStatus(str, Enum):
    PLANNED = "planned"
    CODE_GENERATED = "code_generated"
    VALIDATED = "validated"
    RENDERED = "rendered"
    FAILED = "failed"

class SceneState(BaseModel):
    scene_id: str
    status: SceneStatus
    retries: int = 0
    error_log: str = None
    video_path: str = None

class PipelineState(BaseModel):
    topic: str
    scenes: List[SceneState]
