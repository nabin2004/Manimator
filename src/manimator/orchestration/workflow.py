from orchestration.state import SceneStatus, SceneState, PipelineState
from runtime.resolve import run_runtime

MAX_RETRIES = 3

def execute_pipeline(llm, plan, output_dir: str) -> PipelineState:
    # initialize pipeline state
    pipeline_state = PipelineState(
        topic=plan.topic,
        scenes=[SceneState(scene_id=s.scene_id, status=SceneStatus.PLANNED) for s in plan.scenes]
    )

    for i, scene in enumerate(plan.scenes):
        state = pipeline_state.scenes[i]
        scene_file = f"{output_dir}/{scene.scene_id}.py"

        # 1. Transition: PLANNED → CODE_GENERATED
        state.status = SceneStatus.CODE_GENERATED

        # 2. Execute runtime with repair loop
        try:
            video_paths = run_runtime(llm, [scene_file], output_dir)
            state.video_path = video_paths[0]
            state.status = SceneStatus.RENDERED
        except Exception as e:
            state.error_log = str(e)
            state.retries += 1
            if state.retries < MAX_RETRIES:
                # retry the scene
                state.status = SceneStatus.PLANNED
                # optional: log retry attempt
            else:
                state.status = SceneStatus.FAILED

    return pipeline_state
