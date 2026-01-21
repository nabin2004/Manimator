import os
from runtime.render import render_scene
from runtime.repair import repair_scene
from runtime.validate import validate_scene_code

def run_runtime(llm, scene_files: list, output_dir: str):
    rendered_videos = []

    for scene_file in scene_files:
        with open(scene_file, "r") as f:
            scene_code = f.read()

        # validate
        try:
            validate_scene_code(scene_code)
        except Exception:
            scene_code = repair_scene(llm, scene_file, scene_code)
            # write repaired code
            with open(scene_file, "w") as f:
                f.write(scene_code)

        # render
        video_path = render_scene(scene_file, output_dir)
        rendered_videos.append(video_path)

    return rendered_videos
