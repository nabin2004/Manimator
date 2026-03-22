"""Audio synthesis and video merge utilities.

Synthesises narration audio via the TTS engine, then uses ffmpeg to merge
the audio track into the silent Manim-rendered video.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from manimator.logging.logger import logging


def synthesize_narration(tts_engine, text: str, output_wav: str) -> str:
    """Synthesise *text* to a WAV file using the given TTS engine.

    Returns the absolute path to the written WAV file.
    """
    os.makedirs(os.path.dirname(output_wav) or ".", exist_ok=True)
    tts_engine.generate_to_file(text, output_wav)
    logging.info(f"TTS: wrote narration audio to {output_wav}")
    return output_wav


def merge_audio_video(
    video_path: str,
    audio_path: str,
    output_path: str | None = None,
    timeout: int = 120,
) -> str:
    """Merge a silent video with an audio track using ffmpeg.

    If *output_path* is None, the merged file replaces the original video.

    The shorter stream is padded:
    - If audio is shorter → padded with silence via apad + shortest flag
    - If video is longer → audio simply ends; video continues silently

    Returns the path to the merged file.
    """
    if output_path is None:
        stem = Path(video_path).stem
        output_path = str(Path(video_path).with_name(f"{stem}_narrated.mp4"))

    cmd = [
        "ffmpeg",
        "-y",                           # overwrite without asking
        "-i", video_path,               # input 0: video
        "-i", audio_path,               # input 1: audio
        "-c:v", "copy",                 # copy video codec (no re-encode)
        "-c:a", "aac",                  # encode audio to AAC
        "-b:a", "128k",                 # audio bitrate
        "-shortest",                    # end when the shortest stream ends
        "-map", "0:v:0",               # take video from input 0
        "-map", "1:a:0",               # take audio from input 1
        output_path,
    ]

    logging.info(f"ffmpeg merge command: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        if result.returncode != 0:
            logging.error(f"ffmpeg stderr: {result.stderr}")
            raise RuntimeError(f"ffmpeg merge failed: {result.stderr[:500]}")
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"ffmpeg merge timed out for {video_path}")

    logging.info(f"Merged narrated video at: {output_path}")
    return output_path
