import subprocess

def change_resolution(input_file_path, output_file_path, resolution):
    command = {
        "ffmpeg",
        "-i", input_file_path,
        "-vf", f"scale={resolution}",
        "-vcodec", "libx264",
        "-acodec", "aac",
        output_file_path
    }

    try:
        subprocess.run(command, check=True)
        print(f"Resolution change completed: {output_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during resolution change: {e}")