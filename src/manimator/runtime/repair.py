from manimator.runtime.validate import validate_scene_code

MAX_RETRIES = 3

def repair_scene(llm, scene_file: str, scene_code: str):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            validate_scene_code(scene_code)
            # Optionally, test-run scene before returning
            return scene_code  # valid
        except Exception as e:
            error_log = str(e)
            # ask LLM to fix ONLY the broken code
            prompt = f"""
            Scene code failed validation:
            Error: {error_log}
            Scene code:
            {scene_code}

            Fix the code. Only return Python code, no explanation.
            """
            scene_code = llm.invoke(prompt, phase="scene_repair")
            retries += 1

    raise RuntimeError(f"Scene failed after {MAX_RETRIES} retries")
