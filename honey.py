
def commands(data):
    # This is the honey function
    # It will be called when the honeypot is triggered
    # It will send a fake response to the client
    # and then close the connection
    response = ""

    if data == 'whoami':
        response = 'anadolufs'

    return response


# data = """__  _______         _
# \ \/ /_   _|__  ___| |__
#  \  /  | |/ _ \/ __| '_ \\
#  /  \  | |  __/ (__| | | |
# /_/\_\ |_|\___|\___|_| |_|


#  ____            _
# / ___| _   _ ___| |_ ___ _ __ ___
# \___ \| | | / __| __/ _ \ '_ ` _ \\
#  ___) | |_| \__ \ ||  __/ | | | | |
# |____/ \__, |___/\__\___|_| |_| |_|
#        |___/

# Unauthorized access is prohibited.
# Only authorized individuals are permitted to access and
# access attempts are being recorded. This system belongs
# to X Tech System. If you are not an authorized user,
# DISCONNECT IMMEDIATELY.

# Unauthorized Access is punishable under Articles 243, 244,
# 245, and 246 of the Turkish Penal Code.

# # """


# if command == 'whoami':
#     data="anadolufs\n# "
#     honeypot_socket.send(data.encode())
#     log = "|"+str(datetime.datetime.now()) + "|Honeypot data|whoami"
#     logging.debug(log)

# elif command == 'id':
#     data="uid=1003(anadolufs) gid=1003(anadolufs) groups=1002(admins),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev)\n# "
#     honeypot_socket.send(data.encode())

# elif command == 'ls':
#     data="backup  Desktop  Documents  Public  Templates\n# "
#     honeypot_socket.send(data.encode())
#     log = "|"+str(datetime.datetime.now()) + "|Honeypot data|ls"


# elif command == 'ifconfig' or command=="ip a":
#     data="""\neth0      Link encap:Ethernet  HWaddr 00:00:00:12:e1:a5
# inet addr:192.168.1.5 Bcast:192.168.1.255  Mask:255.255.255.0
# UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
# RX packets:54071 errors:1 dropped:0 overruns:0 frame:0
# TX packets:48515 errors:0 dropped:0 overruns:0 carrier:0
# collisions:0 txqueuelen:1000
# RX bytes:22009423 (20.9 MiB)  TX bytes:25690847 (24.5 MiB)
# Interrupt:10 Base address:0xd020 \n# """
#     honeypot_socket.send(data.encode())


# elif command == 'ps':
#     data="""PID TTY          TIME CMD
# 11130 pts/0    00:00:00 ysh
# 21111 pts/0    00:00:00 ps\n# """
#     honeypot_socket.send(data.encode())

# elif command == 'help':
#     data = """whoami id ps ls ifconfig\n# """
#     honeypot_socket.send(data.encode())
# else:
#     data = f"""ysh: 3: {command.split(" ")[0]}: not found\n# """
#     honeypot_socket.send(data.encode())
# command = ""
