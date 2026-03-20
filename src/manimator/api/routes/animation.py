"""Animation pipeline endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from manimator.api.dependencies import get_llm
from manimator.api.schemas import GenerateRequest, GenerateResponse, SceneResult
from manimator.intent.resolve import resolve_intent
from manimator.planner.resolve import plan_topic
from manimator.orchestration.langgraph_pipeline import run_pipeline

router = APIRouter(prefix="/api/animation", tags=["animation"])


@router.post("/generate", response_model=GenerateResponse)
def generate_animation(req: GenerateRequest):
    """Run the full intent → plan → codegen → validate → render pipeline."""
    llm = get_llm()
    try:
        intent = resolve_intent(req.topic, llm=llm)
        plan = plan_topic(intent, llm=llm)
        state = run_pipeline(llm=llm, plan=plan, output_dir=req.output_dir)

        scenes = []
        for s in state["scenes"]:
            scenes.append(SceneResult(
                scene_id=s["scene_id"],
                status=s["status"],
                video_path=s.get("video_path"),
                error_log=s.get("error_log"),
            ))

        return GenerateResponse(topic=state["topic"], scenes=scenes)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/health")
def animation_health():
    return {"status": "ok", "service": "animation"}
