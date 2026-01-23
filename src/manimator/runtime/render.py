import subprocess
import os
from pathlib import Path
from manimator.logging.logger import logging

def render_scene(scene_file: str, output_dir: str, timeout: int = 60):
    """
    Renders a Manim scene file in a subprocess.
    Returns path to generated video.
    """
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Starting rendering for scene file: {scene_file}")
    logging.info(f"Output directory: {output_dir}")
    scene_name = Path(scene_file).stem
    logging.info(f"Scene name: {scene_name}")
    video_path = os.path.join(output_dir, f"{scene_name}.mp4")
    logging.info(f"Expected video path: {video_path}")

    cmd = [
        "manim",
        "-pql",               # preview quality low for fast rendering
        scene_file,
        "--media_dir", output_dir
    ]
    logging.info(f"Render command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, stdout=None, stderr=None, text=True, timeout=timeout)
        logging.info(f"Render stdout: {result.stdout}")
        logging.info(f"Render stderr: {result.stderr}")
        if result.returncode != 0:
            raise RuntimeError(f"Render failed: {result.stderr}")
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"Rendering timed out for {scene_file}")
    logging.info(f"Rendering completed for scene file: {scene_file}")
    return video_path
