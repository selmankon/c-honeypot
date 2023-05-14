from socket import socket, timeout, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from signal import signal, SIGINT
import logging
import sys
from settings import BUFFER_SIZE, SERVER_HOST, SERVER_PORT, LOG_FILE, BANNER, SHELL_PROMPT
from cmd import run_command


class HoneypotServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.logger = self._setup_logger()
        signal(SIGINT, self.signal_handler)

        try:
            self.server_socket = self._setup_socket(host, port)
            self.logger.info(f'Listening on {host}:{port}...')
        except Exception as e:
            self.logger.error(
                f'Unable to create honeypot server({host}:{port}). {e}')
            self.signal_handler(None, None, None)

    def signal_handler(self, sig, frame, client_socket=None):
        self.logger.info("Exiting...")
        try:
            client_socket.close()
            self.logger.info(f'Client connection has been closed.')
        except:
            pass
        try:
            self.server_socket.close()
            self.logger.info(
                f'Honeypot server({self.host}:{self.port}) has been closed.')
        except:
            pass
        sys.exit(0)

    def run(self):
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                # Telnet default timeout value: 60sec
                client_socket.settimeout(20)
                self.logger.info(
                    f'Client({client_address[0]}:{client_address[1]}) has connected.')
            except Exception as e:
                self.logger.error(f'Unable to accept client connection. {e}')
                self.signal_handler(None, None, client_socket)

            try:
                banner = BANNER
                client_socket.sendall(banner.encode(
                    "utf-8", "backslashreplace"))

                while True:
                    client_socket.sendall(SHELL_PROMPT)
                    data = client_socket.recv(BUFFER_SIZE)
                    if not data:    # If there is no data, the client has disconnected
                        break

                    self.logger.debug(
                        f'Received {data} from {client_address[0]}:{client_address[1]}.')
                    data = data.strip().decode("utf-8", "backslashreplace")

                    response = run_command(data)
                    if response:
                        client_socket.sendall(response)
                        self.logger.debug(
                            f'Sending {response} to {client_address[0]}:{client_address[1]}.')
            except timeout as e:
                self.logger.info(
                    f'Client({client_address[0]}:{client_address[1]}) has timed out.')
            except UnicodeError as e:
                self.logger.error(
                    f'Unable to decode client({client_address[0]}:{client_address[1]}) data. {e}')
            except Exception as e:
                self.logger.error(
                    f'Unable to communicate with client({client_address[0]}:{client_address[1]}). {e}')
            finally:
                client_socket.close()
                self.logger.info(
                    f'Client({client_address[0]}:{client_address[1]}) has disconnected.')

    @ staticmethod
    def _setup_socket(host, port):
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()
        return server_socket

    @ staticmethod
    def _setup_logger():
        logger = logging.getLogger("honeypot_server")
        logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(LOG_FILE)
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            fmt="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s", datefmt="%d/%b/%Y %H:%M:%S")

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger


if __name__ == "__main__":
    honeypot_server = HoneypotServer(SERVER_HOST, SERVER_PORT)
    honeypot_server.run()
