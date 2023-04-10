import socket
import signal
import sys
import logging
import honey

LHOST = "127.0.0.1"  # Honeypot Server IP
LPORT = 65400   # Honeypot Server port
RHOST = "127.0.0.1"  # Dashboard IP
RPORT = 65420   # Dashboard port
BUFFER_SIZE = 1024


def signal_handler(sig, frame):  # Signal handler for Ctrl+C
    print()
    logger.info('Exiting...')
    try:
        client_socket.close()
        logger.info(f'Client connection has been closed')
    except:
        pass
    try:
        dashboard_socket.close()
        logger.info(f'Dashboard({RHOST}:{RPORT}) connection has been closed')
    except:
        pass
    try:
        server_socket.close()
        logger.info(f'Honeypot server({LHOST}:{LPORT}) has been closed')
    except:
        pass
    sys.exit(0)


def setup_logging():    # Setup logging
    global logger

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("server.log")
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def dashboard_log(command):   # Format the data for the dashboard
    # Format: <timestamp> <honey_id> <client_ip> <client_port> <command>
    pass


signal.signal(signal.SIGINT, signal_handler)    # Register the signal handler

setup_logging()  # Setup logging

try:
    server_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)   # Create a TCP socket for the honeypot server
    # Bind the socket to the honeypot server
    server_socket.bind((LHOST, LPORT))
    server_socket.listen()  # Listen for connections
    logger.info(f'Listening on {LHOST}:{LPORT}')
except Exception as e:
    logger.error(f'Unable to create honeypot server({LHOST}:{LPORT}). {e}')
    signal_handler(None, None)

try:
    dashboard_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)   # Create a TCP socket for the dashboard
    dashboard_socket.connect((RHOST, RPORT))  # Connect to the dashboard server
    logger.info(f'Connected to dashboard({RHOST}:{RPORT})')
except Exception as e:
    logger.error(f'Unable to connect dashboard server({LHOST}:{LPORT}). {e}')
    signal_handler(None, None)

while True:
    # DASHBOARD SOKETİ İLE BAĞLANTI KURULMUŞ MU KONTROL EDİLİR. EĞER BAĞLANTI YOKSA CONNECT İLE KURULUR

    try:
        client_socket, client_socket_address = server_socket.accept()  # Accept a connection
        client_ip, client_port = client_socket_address
        client_address = f'{client_ip}:{client_port}'
        client_socket.settimeout(20)    # Set a timeout for the client
    except Exception as e:
        logger.error(f'Unable to accept connection. {e}')
        signal_handler(None, None)  # Exit the program

    try:
        logger.info(f'Connection from {client_address}')

        banner = "Hello World"
        # Send banner data to the client
        client_socket.sendall(banner.encode("utf-8"))

        while True:
            # Receive data from the client
            data = client_socket.recv(BUFFER_SIZE)
            if not data:    # If there is no data, the client has disconnected
                break

            data = data.strip().decode("utf-8")
            logger.debug(f'Received {data} from {client_address}')

            # Send log to the dashboard
            log = dashboard_log(data)
            dashboard_socket.sendall(log.encode("utf-8"))
            logger.debug(f'Sending {log} to dashboard({RHOST}:{RPORT})')

            # Send the data to the honey function
            response = honey.commands(data)
            if response:
                client_socket.sendall(response.encode("utf-8"))
                logger.debug(f'Sending {response} to {client_address}')

    except socket.timeout as e:
        logger.info(f'Connection timeout for {client_address}')
    except UnicodeError as e:
        logger.error(f'Unicode Error: {e}')
    except Exception as e:
        logger.error(f'Client Exception: {e}')
    finally:
        client_socket.close()
        logger.info(f'Connection from {client_address} has been closed')
