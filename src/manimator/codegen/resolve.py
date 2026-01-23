import os
from manimator.codegen.llm_codegen import generate_scene_code
from manimator.codegen.validate import validate_python_code

def generate_code_for_plan(llm, plan, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    generated_files = []

    for scene in plan.scenes:
        code = generate_scene_code(llm, scene)

        with open(os.path.join(output_dir, f"{scene.scene_id}.py"), "w") as f:
            f.write(code)
            print(f"Wrote code for scene {scene.scene_id} to {f.name}")

        validate_python_code(code)

        filepath = os.path.join(output_dir, f"{scene.scene_id}.py")
        with open(filepath, "w") as f:
            f.write(code)
        generated_files.append(filepath)

    return generated_files
