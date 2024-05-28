import socket
import struct
import os

HOST = 'localhost'
PORT = 8888
BUFFER_SIZE = 1400

ROOT_DIR = os.path.dirname(__file__)
VIDEOS_DIR = os.path.join(ROOT_DIR, 'videos')

def select_file():
    print("Available files:")
    files = os.listdir(VIDEOS_DIR)
    for i, file in enumerate(files, start=1):
        print(f"{i}: {file}")

    while True:
        try:
            choice = int(input("Select a file: "))
            if 1 <= choice <= len(files):
                return os.path.join(VIDEOS_DIR, files[choice - 1])
            else:
                print("Invalid choice. Please select a valid file number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    selected_file = select_file()

    print("1: Compress Video.")
    print("2: Change resolution.")
    print("3: Change the aspect ratio.")
    print("4: Change to audio.")
    print("5: Create GIF or WEBM.")
    option = input("Select from options: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Send processing option to the server
    client_socket.sendall(option.encode('utf-8'))

    file_size = os.path.getsize(selected_file)
    print(f"Send file size: {file_size} bytes")
    file_size_data = struct.pack('!I', file_size)
    client_socket.sendall(file_size_data)

    with open(selected_file, 'rb') as file:
        while True:
            chunk = file.read(BUFFER_SIZE)
            if not chunk:
                break
            client_socket.sendall(chunk)

    status = client_socket.recv(16)
    if status.strip(b'\0') == b'OK':
        print("File processed successfully")
    else:
        print("File processing failed")

    client_socket.close()

if __name__ == '__main__':
    main()
