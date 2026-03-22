from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from typing import List, Optional
from manimator.runtime.resolve import run_runtime
from manimator.runtime.validate import validate_scene_code
from manimator.runtime.repair import repair_scene
from manimator.codegen.resolve import generate_code_for_plan
from manimator.narration.narrate import generate_narration
from manimator.runtime.audio_merge import synthesize_narration, merge_audio_video
from manimator.api.dependencies import get_tts_engine

MAX_RETRIES = 3

# ----------------------------
# Define state model for LangGraph
# ----------------------------
class SceneStateLG(BaseModel):
    scene_id: str
    status: str = "PLANNED"
    retries: int = 0
    error_log: Optional[str] = None
    video_path: Optional[str] = None
    narration: Optional[str] = None
    audio_path: Optional[str] = None


class PipelineStateLG(BaseModel):
    topic: str
    scenes: List[SceneStateLG]
    output_dir: str


# ----------------------------
# Define nodes
# ----------------------------

def codegen_node(state, llm, plan):
    generate_code_for_plan(llm, plan, state.output_dir)

    for scene in state.scenes:
        scene.status = "CODE_GENERATED"
    return state

def validate_node(state):
    for scene in state.scenes:
        scene_file = f"{state.output_dir}/{scene.scene_id}.py"
        try:
            validate_scene_code(open(scene_file).read())
            scene.status = "VALIDATED"
        except Exception as e:
            scene.error_log = str(e)
            scene.status = "FAILED"
    return state

def repair_node(state, llm):
    for scene in state.scenes:
        if scene.status == "FAILED" and scene.retries < MAX_RETRIES:
            scene_file = f"{state.output_dir}/{scene.scene_id}.py"
            code = open(scene_file).read()
            fixed_code = repair_scene(llm, scene_file, code)
            # write fixed code back
            with open(scene_file, "w") as f:
                f.write(fixed_code)
            scene.retries += 1
            scene.status = "CODE_GENERATED"  # retry path
    return state

def render_node(state, llm):
    for scene in state.scenes:
        if scene.status == "VALIDATED" or (scene.status == "CODE_GENERATED" and scene.retries > 0):
            scene_file = f"{state.output_dir}/{scene.scene_id}.py"
            try:
                videos = run_runtime(llm, [scene_file], state.output_dir)
                scene.video_path = videos[0]
                scene.status = "RENDERED"
            except Exception as e:
                scene.error_log = str(e)
                scene.retries += 1
                scene.status = "FAILED"
        else:
            print(f"Skipping rendering for scene {scene.scene_id} with status {scene.status}")
    return state

def validate_and_route(state, llm):
    for scene in state.scenes:
        scene_file = f"{state.output_dir}/{scene.scene_id}.py"
        try:
            validate_scene_code(open(scene_file).read())
            scene.status = "VALIDATED"
        except Exception:
            scene_code = repair_scene(llm, scene_file, open(scene_file).read())
            with open(scene_file, "w") as f:
                f.write(scene_code)
            scene.status = "CODE_GENERATED"  # retry path
    return state


def narrate_node(state, llm, plan):
    """Generate narration audio and merge it with each rendered scene video."""
    import os

    tts_engine = get_tts_engine()

    # Build a lookup from scene_id to the planner's SceneSpec
    scene_specs = {s.scene_id: s for s in plan.scenes}

    for scene in state.scenes:
        if scene.status != "RENDERED" or not scene.video_path:
            print(f"Skipping narration for scene {scene.scene_id} (status={scene.status})")
            continue

        spec = scene_specs.get(scene.scene_id)
        if not spec:
            print(f"No plan spec found for scene {scene.scene_id}, skipping narration")
            continue

        try:
            # 1. Generate narration script via LLM
            print(f"Generating narration for scene {scene.scene_id}...")
            narration_text = generate_narration(llm, spec)
            scene.narration = narration_text
            print(f"Narration ({len(narration_text)} chars): {narration_text[:100]}...")

            # 2. Synthesize to WAV via TTS
            audio_dir = os.path.join(state.output_dir, "audio")
            os.makedirs(audio_dir, exist_ok=True)
            wav_path = os.path.join(audio_dir, f"{scene.scene_id}.wav")
            synthesize_narration(tts_engine, narration_text, wav_path)
            scene.audio_path = wav_path

            # 3. Merge audio + video via ffmpeg
            merged_path = merge_audio_video(scene.video_path, wav_path)
            scene.video_path = merged_path  # update to narrated video
            scene.status = "NARRATED"
            print(f"Scene {scene.scene_id} narrated → {merged_path}")

        except Exception as e:
            print(f"Narration failed for scene {scene.scene_id}: {e}")
            scene.error_log = f"Narration error: {e}"
            # Don't change status — keep RENDERED so the silent video is still usable

    return state


# ----------------------------
# Build LangGraph
# ----------------------------

def build_pipeline_graph(llm, plan, output_dir):
    pipeline_state = PipelineStateLG(
        topic=plan.topic,
        scenes=[SceneStateLG(scene_id=s.scene_id) for s in plan.scenes],
        output_dir=output_dir,
    )
    pipeline_state.output_dir = output_dir

    graph = StateGraph(PipelineStateLG)

    # Add nodes
    graph.add_node("codegen", lambda s: codegen_node(s, llm, plan))
    graph.add_node("validate_and_route", lambda s: validate_and_route(s, llm))
    graph.add_node("render", lambda s: render_node(s, llm))
    graph.add_node("narrate", lambda s: narrate_node(s, llm, plan))

    # Pipeline: codegen → validate → render → narrate → END
    graph.add_edge(START, "codegen")
    graph.add_edge("codegen", "validate_and_route")
    graph.add_edge("validate_and_route", "render")
    graph.add_edge("render", "narrate")
    graph.add_edge("narrate", END)

    return graph, pipeline_state

# ----------------------------
# Run the LangGraph pipeline
# ----------------------------
def run_pipeline(llm, plan, output_dir):
    graph, state = build_pipeline_graph(llm, plan, output_dir)
    compiled = graph.compile()
    final_state = compiled.invoke(state)
    return final_state
