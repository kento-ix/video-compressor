import os
import subprocess

def compress_mp4(directory_path, output_dir, crf=23, audio_bitrate="128k"):

    if not os.path.isdir(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.")
        return
    
    if not os.path.isdir(directory_path):
        print(f"Error: Directory '{output_dir} does not exist.")
        return

    files = os.listdir(directory_path)

    for file in files:
        if file.endswith('.mp4'):
            input_file_path = os.path.join(directory_path, file)
            output_file_path = os.path.join(output_dir, os.path.splitext(file)[0] + "_compressed.mp4")

            command = [
                "ffmpeg",
                "-i", input_file_path,
                "-vcodec", "libx264",
                "-crf", str(crf),
                "-acodec", "aac",
                "-b:a", audio_bitrate,
                output_file_path
            ]

            try:
                subprocess.run(command, check=True)
                print(f"Video compression completed: {output_file_path}")

                # os.remove(input_file_path)
                # print(f"Original file deleted: {input_file_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error during video compression: {e}")

if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.dirname(__file__))  
    video_dir = os.path.join(root_dir, 'videos')
    output_dir = os.path.join(root_dir, 'proceed')
    compress_mp4(video_dir, output_dir)
