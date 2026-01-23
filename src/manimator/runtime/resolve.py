import os
from manimator.runtime.render import render_scene
from manimator.runtime.repair import repair_scene
from manimator.runtime.validate import validate_scene_code
from manimator.logging.logger import logging

def run_runtime(llm, scene_files: list, output_dir: str):
    logging.info(f"Running runtime for scenes: {scene_files}")
    rendered_videos = []

    for scene_file in scene_files:
        with open(scene_file, "r") as f:
            scene_code = f.read()

        # validate
        logging.info(f"Validating scene code from file: {scene_file}")
        try:
            validate_scene_code(scene_code)
        except Exception:
            scene_code = repair_scene(llm, scene_file, scene_code)
            # write repaired code
            with open(scene_file, "w") as f:
                f.write(scene_code)
        logging.info(f"Validation successful for scene file: {scene_file}")

        # render
        logging.info(f"Rendering scene from file: {scene_file}")
        video_path = render_scene(scene_file, output_dir)
        logging.info(f"Rendered video saved at: {video_path}")
        rendered_videos.append(video_path)
        logging.info(f"Completed rendering for scene file: {scene_file}")

    return rendered_videos
