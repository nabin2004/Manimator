from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from typing import List, Literal
from manimator.runtime.resolve import run_runtime
from manimator.runtime.validate import validate_scene_code
from manimator.runtime.repair import repair_scene
from manimator.codegen.resolve import generate_code_for_plan

# Global constant for the "patience" of the agent
MAX_RETRIES = 3

# ----------------------------
# 1. Define State (The Agent's Memory)
# ----------------------------
class SceneStateLG(BaseModel):
    scene_id: str
    status: str = "PLANNED"  # PLANNED, GENERATED, VALIDATED, FAILED, RENDERED
    retries: int = 0
    error_log: str = None
    video_path: str = None

class PipelineStateLG(BaseModel):
    topic: str
    scenes: List[SceneStateLG]
    output_dir: str

# ----------------------------
# 2. Define Nodes (The Agent's Actions)
# ----------------------------

def codegen_node(state: PipelineStateLG, llm, plan):
    """Initial Code Generation."""
    # Only generate if not already generated to avoid overwriting repairs
    if any(s.status == "PLANNED" for s in state.scenes):
        print(f"--- 🤖 Generating Initial Code for {state.topic} ---")
        generate_code_for_plan(llm, plan, state.output_dir)
        for scene in state.scenes:
            if scene.status == "PLANNED":
                scene.status = "GENERATED"
    return state

def validate_node(state: PipelineStateLG):
    """The Inspector: Checks code and logs errors."""
    print("--- 🔍 Validating Code ---")
    for scene in state.scenes:
        # We only validate scenes that need it (Generated or Repaired)
        if scene.status in ["GENERATED", "REPAIRED"]:
            scene_file = f"{state.output_dir}/{scene.scene_id}.py"
            try:
                # Read and check
                code = open(scene_file).read()
                validate_scene_code(code)
                scene.status = "VALIDATED"
                scene.error_log = None # Clear errors if valid
            except Exception as e:
                print(f"❌ Error in {scene.scene_id}: {str(e)[:50]}...")
                scene.error_log = str(e)
                scene.status = "FAILED"
    return state

def repair_node(state: PipelineStateLG, llm):
    """The Fixer: Uses the error log to patch the code."""
    print("--- 🔧 Repairing Failed Scenes ---")
    for scene in state.scenes:
        if scene.status == "FAILED" and scene.retries < MAX_RETRIES:
            scene_file = f"{state.output_dir}/{scene.scene_id}.py"
            code = open(scene_file).read()
            
            # CALL THE REPAIR AGENT
            # Note: We pass the error log implicitly via the repair_scene logic 
            # (Assuming repair_scene prompts the LLM with the code + error)
            fixed_code = repair_scene(llm, scene_file, code)
            
            with open(scene_file, "w") as f:
                f.write(fixed_code)
            
            scene.retries += 1
            scene.status = "REPAIRED" # Mark as repaired so it gets validated again
            print(f"   -> Repaired {scene.scene_id} (Attempt {scene.retries})")
    return state

def render_node(state: PipelineStateLG, llm):
    """The Renderer: Only runs validated code."""
    print("--- 🎥 Rendering Scenes ---")
    for scene in state.scenes:
        if scene.status == "VALIDATED":
            scene_file = f"{state.output_dir}/{scene.scene_id}.py"
            try:
                videos = run_runtime(llm, [scene_file], state.output_dir)
                scene.video_path = videos[0]
                scene.status = "RENDERED"
            except Exception as e:
                # If runtime fails, we could loop back, but for now lets mark failed
                scene.error_log = f"Runtime Error: {str(e)}"
                scene.status = "FAILED"
    return state

# ----------------------------
# 3. The Router (The Agent's Brain)
# ----------------------------

def router(state: PipelineStateLG) -> Literal["repair", "render", "end"]:
    """Decides the next step based on the state of the scenes."""
    
    # Get lists of scenes by status
    failed_scenes = [s for s in state.scenes if s.status == "FAILED"]
    
    # 1. If everything is valid, go to render
    if all(s.status == "VALIDATED" or s.status == "RENDERED" for s in state.scenes):
        return "render"

    # 2. If there are failures...
    if failed_scenes:
        # Check if we have retries left
        if any(s.retries < MAX_RETRIES for s in failed_scenes):
            return "repair" # LOOP BACK!
        else:
            # We ran out of retries for some scenes
            # You might want to render the good ones and skip the bad ones
            return "render"
            
    # Default fallthrough
    return "end"

# ----------------------------
# 4. Build The Graph
# ----------------------------

def build_pipeline_graph(llm, plan, output_dir):
    # Initialize state
    pipeline_state = PipelineStateLG(
        topic=plan.topic,
        scenes=[SceneStateLG(scene_id=s.scene_id) for s in plan.scenes],
        output_dir=output_dir,
    )

    workflow = StateGraph(PipelineStateLG)

    # Add Nodes
    # Using lambda to inject arguments that aren't in the state (llm, plan)
    workflow.add_node("codegen", lambda s: codegen_node(s, llm, plan))
    workflow.add_node("validate", validate_node)
    workflow.add_node("repair", lambda s: repair_node(s, llm))
    workflow.add_node("render", lambda s: render_node(s, llm))

    # Add Edges
    workflow.add_edge(START, "codegen")
    workflow.add_edge("codegen", "validate")
    
    # CONDITIONAL EDGE: The Magic happens here
    # Instead of going straight to render, we ask the router where to go
    workflow.add_conditional_edges(
        "validate", 
        router,
        {
            "repair": "repair",
            "render": "render",
            "end": END
        }
    )
    
    # CLOSE THE LOOP
    # After repairing, go back to validation!
    workflow.add_edge("repair", "validate")
    
    workflow.add_edge("render", END)

    return workflow, pipeline_state

def run_pipeline(llm, plan, output_dir):
    graph, state = build_pipeline_graph(llm, plan, output_dir)
    compiled = graph.compile()
    final_state = compiled.invoke(state)
    return final_state