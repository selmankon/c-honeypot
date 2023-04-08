import socket
import signal
import sys
import logging
import honey

HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 1024


def signal_handler(sig, frame):  # Signal handler for Ctrl+C
    print()
    logger.info("Server shutting down")
    try:
        client_socket.close()
    except:
        pass
    server_socket.close()
    sys.exit(0)


def setup_logging():    # Setup logging
    global logger

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("server.log")
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


signal.signal(signal.SIGINT, signal_handler)    # Register the signal handler

setup_logging()  # Setup logging

server_socket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)   # Create a TCP socket
server_socket.bind((HOST, PORT))    # Bind the socket to the port
server_socket.listen()  # Listen for incoming connections

while True:
    try:
        client_socket, client_socket_address = server_socket.accept()  # Accept a connection
        client_ip, client_port = client_socket_address
        client_address = f'{client_ip}:{client_port}'
        client_socket.settimeout(20)    # Set a timeout for the client
    except Exception as e:
        logger.error(f'Server Exception: {e}')
        signal_handler(None, None)  # Exit the program

    try:
        logger.info(f'Connected by {client_address}')

        data = "Hello World"
        client_socket.sendall(data.encode("UTF-8"))  # Send data to the client

        while True:
            # Receive data from the client
            data = client_socket.recv(BUFFER_SIZE)
            if not data:    # If there is no data, the client has disconnected
                logger.info(f'Connection closed by {client_address}')
                break
            
            data = data.strip().decode("UTF-8")
            logger.debug(f'Received {data} from {client_address}')
            honey.honey(client_socket, data)    # Send the data to the honey function

    except socket.timeout as e:
        logger.info(f'Connection timed out for {client_address}')
    except UnicodeError as e:
        logger.error(f'UnicodeError for {client_address}. {e}')
    except Exception as e:
        logger.error(f'Client Exception: {e}')
    finally:
        client_socket.close()
