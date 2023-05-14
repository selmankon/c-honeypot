BUFFER_SIZE = 1024
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 65400
LOG_FILE = 'honeypot-server.log'
SHELL_PROMPT = b'[DEMO-INC-SERVER-01 ~]# '
BANNER_FILE = 'banner'
BANNER = """
    ========================================
                DEMO INC. SERVER
    ========================================
    # Hostname....: DEMO-INC-SERVER-01
    # IP Address..: 192.168.1.5
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
