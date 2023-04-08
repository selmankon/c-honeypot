import socket
import signal
import sys

HOST = "127.0.0.1"
PORT = 65432


# Signal handler for Ctrl+C
def signal_handler(sig, frame):
    print("\nExiting...")
    server_socket.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)    # Register the signal handler

server_socket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)   # Create a TCP socket
server_socket.bind((HOST, PORT))    # Bind the socket to the port
server_socket.listen()  # Listen for incoming connections

while True:
    try:
        client_socket, client_address = server_socket.accept()  # Accept a connection
        client_socket.settimeout(20)    # Set a timeout for the client
    except Exception as e:
        print("Server Exception: ", e)
        signal_handler(None, None)  # Exit the program

    try:
        print("Connected by", client_address)

        data = "Hello World"
        client_socket.sendall(data.encode("UTF-8"))  # Send data to the client

        while True:
            data = client_socket.recv(1024)  # Receive data from the client
            if not data:    # If there is no data, the client has disconnected
                print("Disconnected", client_address)
                break
            print("Received", data)

    except Exception as e:
        print("Client Exception: ", e)
        client_socket.close()
