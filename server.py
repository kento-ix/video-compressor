import socket
import struct
import os
import shutil
from lib.compressor import compress_mp4
from lib.resolution import change_resolution
from lib.aspect_ratio import change_aspect_ratio
from lib.audio import convert_to_audio
from lib.gif import create_gif
from lib.gif import create_webm

HOST = 'localhost'
PORT = 8888
BUFFER_SIZE = 1400

STATUS_OK = b'OK'.ljust(16, b'\0')
STATUS_ERROR = b'ERROR'.ljust(16, b'\0')

def handle_client(client_socket):
    root_dir = os.path.dirname(__file__)
    videos_dir = os.path.join(root_dir, 'videos')
    proceed_dir = os.path.join(root_dir, 'proceed')
    
    try:
        option = client_socket.recv(1).decode('utf-8')
        file_size_data = client_socket.recv(32)
        file_size = struct.unpack('!I', file_size_data)[0]
        print(f'Receive file size: {file_size} byte')

        received_file_path = os.path.join(videos_dir, 'video.mp4')
        output_file_path = os.path.join(proceed_dir, 'processed_video.mp4')

        with open(received_file_path, 'wb') as file:
            total_received = 0
            while total_received < file_size:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                file.write(data)
                total_received += len(data)

        if option == '1':
            compress_mp4(received_file_path, output_file_path)
        elif option == '2':
            resolution = input("Enter the desired resolution (e.g., 1280x720): ")
            change_resolution(received_file_path, output_file_path, resolution)
        elif option == '3':
            aspect_ratio = input("Enter the desired aspect ratio (e.g., 16:9): ")
            change_aspect_ratio(received_file_path, output_file_path, aspect_ratio)
        elif option == '4':
            output_file_path = os.path.join(proceed_dir, 'processed_audio.mp3')
            convert_to_audio(received_file_path, output_file_path)
        elif option == '5':
            format_choice = input("Enter the desired format (gif/webm): ")
            scale = input("Enter the desired scale (default: 320:-1): ") or '320:-1'
            fps = input("Enter the desired fps (default: 15): ") or 15
            if format_choice == 'gif':
                output_file_path = os.path.join(proceed_dir, 'processed_video.gif')
                create_gif(received_file_path, output_file_path, scale, fps)
            elif format_choice == 'webm':
                output_file_path = os.path.join(proceed_dir, 'processed_video.webm')
                create_webm(received_file_path, output_file_path, scale, fps)
            else:
                client_socket.sendall(STATUS_ERROR)
                return
        else:
            client_socket.sendall(STATUS_ERROR)
            return

        client_socket.sendall(STATUS_OK)

        # Move the processed file to the proceed directory
        shutil.move(received_file_path, output_file_path)
        
    except Exception as e:
        print('Error: ', e)
        client_socket.sendall(STATUS_ERROR)
    finally:
        client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print('Activate server')

    while True:
        client_socket, address = server_socket.accept()
        print('Accept connection: ', address)
        handle_client(client_socket)

if __name__ == '__main__':
    main()
