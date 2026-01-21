from orchestration.workflow import execute_pipeline

def run_full_pipeline(llm, script_plan, output_dir: str):
    """
    End-to-end orchestration:
    - Executes scenes
    - Handles retries
    - Returns full pipeline state
    """
    pipeline_state = execute_pipeline(llm, script_plan, output_dir)
    return pipeline_state
