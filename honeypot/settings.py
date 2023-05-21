# Server/Socket Settings
BUFFER_SIZE = 1024
CONNECTION_TIMEOUT = 6000  # Telnet default timeout value: 60sec
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 65400
LOG_FILE = 'honeypot-server.log'


# Honeypot/Linux Settings
POT_HOSTNAME = 'DEMO-INC-SERVER-02'
POT_USERNAME = 'anadolufs'
POT_IP = '192.168.4.132'
POT_BROADCAST = '192.168.4.135'
POT_MASK = '255.255.255.248'
SHELL_PROMPT = f'[{POT_HOSTNAME} ~]# '
BANNER = f"""
    ========================================
                DEMO INC. SERVER
    ========================================
    # Hostname....: {POT_HOSTNAME}
    # IP Address..: {POT_IP}
    # OS Version..: Debian 10.0
    # Uptime......: 1 day(s), 02h 03m 41s
    ========================================
            Authorized access only!
      Disconnect IMMEDIATELY if you are not
              an authorized user!
        All actions will be monitored and
                    recorded!
    ========================================

"""
