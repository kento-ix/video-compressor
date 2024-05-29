import subprocess

def change_aspect_ratio(input_file_path, output_file_path, aspect_ratio):
    """
    Change the aspect ratio of an MP4 file.

    Parameters:
    input_file_path (str): The path to the input MP4 file.
    output_file_path (str): The path to the output MP4 file.
    aspect_ratio (str): The desired aspect ratio (e.g., "16:9").
    """
    command = [
        "ffmpeg",
        "-i", input_file_path,
        "-vf", f"setsar={aspect_ratio}",
        "-c:a", "copy",
        output_file_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Aspect ratio change completed: {output_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during aspect ratio change: {e}")
