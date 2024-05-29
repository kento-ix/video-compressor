import os
import subprocess

def convert_to_audio(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-vn",
        "-acodec", "mp3",
        output_file
    ]
    subprocess.run(command, check=True)
