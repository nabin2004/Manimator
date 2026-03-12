import subprocess
from pathlib import Path

# Root directory to scan
VIDEO_ROOT = Path("storage/videos")

# Find all .mp4 files recursively, excluding any in 'partial_movie_files' directories
video_files = sorted(
    f for f in VIDEO_ROOT.rglob("*.mp4")
    if "partial_movie_files" not in f.parts
)

if not video_files:
    print("No MP4 files found!")
    exit(0)

print(f"Found {len(video_files)} final videos. Playing one by one...")

for idx, video_path in enumerate(video_files, start=1):
    print(f"\n[{idx}/{len(video_files)}] Playing: {video_path}")
    try:
        # ffplay command: auto-exit when done, no display needed
        subprocess.run(
            ["ffplay", str(video_path)],
            check=True
        )
    except subprocess.CalledProcessError:
        print(f"Failed to play {video_path}, skipping...")
    except KeyboardInterrupt:
        print("Playback interrupted by user. Exiting.")
        break