from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from typing import List
from manimator.runtime.resolve import run_runtime
from manimator.runtime.validate import validate_scene_code
from manimator.runtime.repair import repair_scene
from manimator.codegen.resolve import generate_code_for_plan

MAX_RETRIES = 3

# ----------------------------
# Define state model for LangGraph
# ----------------------------
class SceneStateLG(BaseModel):
    scene_id: str
    status: str = "PLANNED"
    retries: int = 0
    error_log: str = None
    video_path: str = None

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
    return state

# ----------------------------
# Build LangGraph
# ----------------------------

def build_pipeline_graph(llm, plan, output_dir):
    # Initialize pipeline state
    pipeline_state = PipelineStateLG(
        topic=plan.topic,
        scenes=[SceneStateLG(scene_id=s.scene_id) for s in plan.scenes],
        output_dir=output_dir,
    )
    # store output_dir in state
    pipeline_state.output_dir = output_dir

    graph = StateGraph(PipelineStateLG)

    # Add nodes
    graph.add_node("codegen", lambda s: codegen_node(s, llm, plan))
    graph.add_node("validate", validate_node)
    graph.add_node("repair", lambda s: repair_node(s, llm))
    graph.add_node("render", lambda s: render_node(s, llm))

    # Add edges
    graph.add_edge(START, "codegen")
    graph.add_edge("codegen", "validate")
    graph.add_edge("validate", "render")
    graph.add_edge("validate", "repair")   # failed validation goes to repair
    graph.add_edge("repair", "codegen")    # retry after repair
    graph.add_edge("render", END)

    return graph, pipeline_state

# ----------------------------
# Run the LangGraph pipeline
# ----------------------------
def run_pipeline(llm, plan, output_dir):
    graph, state = build_pipeline_graph(llm, plan, output_dir)
    compiled = graph.compile()
    final_state = compiled.invoke(state)
    return final_state
