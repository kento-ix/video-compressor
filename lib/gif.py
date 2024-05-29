import os
import subprocess

def create_gif(input_file, output_file, scale='320:-1', fps=15):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-vf", f"fps={fps},scale={scale}",
        output_file
    ]
    subprocess.run(command, check=True)

def create_webm(input_file, output_file, scale='320:-1', fps=15):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-vf", f"fps={fps},scale={scale}",
        "-c:v", "libvpx",
        "-b:v", "1M",
        "-c:a", "libvorbis",
        output_file
    ]
    subprocess.run(command, check=True)
