import subprocess
import os
import glob
from pathlib import Path
from manimator.logging.logger import logging

def render_scene(scene_file: str, output_dir: str, timeout: int = 120):
    """
    Renders a Manim scene file in a subprocess.
    Returns path to generated video.
    """
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Starting rendering for scene file: {scene_file}")
    logging.info(f"Output directory: {output_dir}")
    scene_name = Path(scene_file).stem
    logging.info(f"Scene name: {scene_name}")

    cmd = [
        "manim",
        "-ql",               # quality low for fast rendering, NO preview
        scene_file,
        "--media_dir", output_dir
    ]
    logging.info(f"Render command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        logging.info(f"Render stdout: {result.stdout}")
        logging.info(f"Render stderr: {result.stderr}")
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"Rendering timed out for {scene_file}")

    # Manim outputs to: {media_dir}/videos/{SceneName}/{quality}/{SceneClass}.mp4
    # Search for the actual video file instead of guessing the path
    video_pattern = os.path.join(output_dir, "videos", "**", "*.mp4")
    found = glob.glob(video_pattern, recursive=True)
    # Filter to videos matching our scene name (case-insensitive)
    scene_videos = [v for v in found if scene_name.lower() in Path(v).stem.lower()]

    if scene_videos:
        # Take the newest match
        video_path = max(scene_videos, key=os.path.getmtime)
        logging.info(f"Found rendered video at: {video_path}")
        return video_path

    # If no matching video was found, the render truly failed
    if result.returncode != 0:
        raise RuntimeError(f"Render failed (exit {result.returncode}): {result.stderr}")
    
    # Fallback: return the original expected path
    video_path = os.path.join(output_dir, f"{scene_name}.mp4")
    logging.info(f"Rendering completed for scene file: {scene_file}")
    return video_path
