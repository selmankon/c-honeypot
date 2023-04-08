import socket
import signal
import sys

HOST = "127.0.0.1"
PORT = 65432


def signal_handler(sig, frame):
    print("\nExiting...")
    server_socket.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

while True:
    try:
        client_socket, client_address = server_socket.accept()
        client_socket.settimeout(20)
    except Exception as e:
        print("Server Exception: ", e)
        signal_handler(None, None)

    try:
        print("Connected by", client_address)

        data = "Hello World"
        client_socket.sendall(data.encode("UTF-8"))

        while True:
            data = client_socket.recv(1024)
            if not data:
                print("Disconnected", client_address)
                break
            print("Received", data)

    except Exception as e:
        print("Client Exception: ", e)
        client_socket.close()
