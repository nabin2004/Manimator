import subprocess
import os
from pathlib import Path

def render_scene(scene_file: str, output_dir: str, timeout: int = 60):
    """
    Renders a Manim scene file in a subprocess.
    Returns path to generated video.
    """
    os.makedirs(output_dir, exist_ok=True)
    scene_name = Path(scene_file).stem
    video_path = os.path.join(output_dir, f"{scene_name}.mp4")

    cmd = [
        "manim",
        "-pql",               # preview quality low for fast rendering
        scene_file,
        "--media_dir", output_dir
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            raise RuntimeError(f"Render failed: {result.stderr}")
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"Rendering timed out for {scene_file}")

    return video_path
