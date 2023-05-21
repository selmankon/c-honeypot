from settings import POT_HOSTNAME, POT_IP, POT_BROADCAST, POT_MASK, POT_USERNAME


def check_command(command, workdir, client_address=None, logger=None):
    try:
        if command.startswith("cd"):
            response, workdir = cd_command(
                command, workdir, client_address, logger)
        elif command == "exit" or command == "quit" or command == "logout":
            response = True
        elif command == "help":
            response = help_command()
        elif command == "hostname":
            response = hostname_command()
        elif command == "id":
            response = id_command()
        elif command == "ifconfig":
            response = ifconfig_command()
        elif command.startswith("ls"):
            response = ls_command(command, workdir)
        elif command == "ps":
            response = ps_command()
        elif command == "pwd":
            response = pwd_command(workdir)
        elif command == "whoami":
            response = whoami_command()
        else:
            response = permission_denied(command)
    except Exception as e:
        logger.error(
            f"Error while executing command '{command}' on {client_address[0]}:{client_address[1]}. {e}")
        response = command_not_found(command)
    return response, workdir


def command_not_found(command):
    response = f"""/bin/ysh: {command}: not found\n"""
    return response


def permission_denied(command):
    response = f"""/bin/ysh: {command}: Permission denied\n"""
    return response


def no_such_file_or_directory(command):
    response = f"""/bin/ysh: {command}: No such file or directory\n"""
    return response


def cd_command(command, workdir, client_address=None, logger=None, from_ls=False):
    old_workdir = workdir
    new_workdir = workdir
    directory_list = ["/home", f"/home/{POT_USERNAME}",
                      f"/home/{POT_USERNAME}/backup", f"/home/{POT_USERNAME}/Desktop", f"/home/{POT_USERNAME}/Documents", f"/home/{POT_USERNAME}/Downloads", f"/home/{POT_USERNAME}/Public", f"/home/{POT_USERNAME}/Templates"]

    command_split = command.split(" ")
    if len(command_split) == 1:
        return command_not_found(command), old_workdir

    command_prefix = command_split[0]
    command_params = command_split[1]

    if command_params.startswith(".."):
        if workdir == "/home":
            return permission_denied(command), old_workdir

        command_params = command_params.replace("..", "", 1)
        new_workdir = workdir.split("/")
        new_workdir.pop()
        new_workdir = "/".join(new_workdir)

        if command_params.startswith("/"):
            new_workdir = f"""{new_workdir}{command_params}"""
        else:
            new_workdir = f"""{new_workdir}/{command_params}"""
    elif command_params.startswith("."):
        command_params = command_params.replace(".", "", 1)
        if command_params.startswith("/"):
            new_workdir = f"""{workdir}{command_params}"""
        else:
            new_workdir = f"""{workdir}/{command_params}"""
    elif command_params.startswith("/"):
        return permission_denied(command), old_workdir
    elif command_params.startswith("~"):
        command_params = command_params.replace("~", "", 1)
        if command_params.startswith("/"):
            new_workdir = f"""/home/{POT_USERNAME}{command_params}"""
        else:
            new_workdir = f"""/home/{POT_USERNAME}/{command_params}"""
    else:
        new_workdir = f"""{workdir}/{command_params}"""

    if new_workdir.endswith("/"):
        new_workdir = new_workdir[:-1]

    if new_workdir in directory_list:
        response = """"""
        if not from_ls:
            logger.debug(
                f'Changing directory from {old_workdir} to {new_workdir} on {client_address[0]}:{client_address[1]}.')
    else:
        return no_such_file_or_directory(command), old_workdir

    return response, new_workdir


def help_command():
    response = """hostname id ifconfig ls ps pwd whoami\n"""
    return response


def hostname_command():
    response = f"""{POT_HOSTNAME}\n"""
    return response


def id_command():
    response = f"""uid=1003({POT_USERNAME}) gid=1003({POT_USERNAME}) groups=1002(admins),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev)\n"""
    return response


def ifconfig_command():
    response = f"""eth0      Link encap:Ethernet  HWaddr 02:42:AC:11:00:02
          inet addr:{POT_IP}  Bcast:{POT_BROADCAST}  Mask:{POT_MASK}
          UP BROADCAST RUNNING MULTICAST  MTU:65535  Metric:1
          RX packets:54071 errors:2 dropped:0 overruns:0 frame:0
          TX packets:48515 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:22009423 (20.9 MiB)  TX bytes:25690847 (24.5 MiB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)\n"""
    return response


def ls_command(command, workdir):
    if command == "ls":
        if workdir == f"/home":
            response = f"""total 12
drwxr-xr-x    1 root          {POT_USERNAME}          4096 May 21 14:26 .
drwxr-x--x    1 root          root               4096 May 21 14:26 ..
drwxr-xr-x    1 {POT_USERNAME}     {POT_USERNAME}          4096 May  9 18:42 {POT_USERNAME}\n"""
        elif workdir == f"/home/{POT_USERNAME}":
            response = f"""total 36
drwxr-xr-x    1 {POT_USERNAME}     {POT_USERNAME}          4096 May 21 14:26 .
drwxr-xr-x    1 root          {POT_USERNAME}          4096 May 21 14:26 ..
drwxr-xr-x    1 {POT_USERNAME}     {POT_USERNAME}          4096 May 15 20:44 backup
drwxr-xr-x    5 {POT_USERNAME}     {POT_USERNAME}           360 May 21 14:26 Desktop
drwxr-xr-x    1 {POT_USERNAME}     {POT_USERNAME}          4096 May 21 14:26 Documents
drwxr-xr-x    2 {POT_USERNAME}     {POT_USERNAME}          4096 May  9 18:42 Public
drwxr-xr-x    1 {POT_USERNAME}     {POT_USERNAME}          4096 May  9 18:42 Templates\n"""
        elif workdir == f"/home/{POT_USERNAME}/backup":
            response = f"""total 8
drwxr-xr-x    1 {POT_USERNAME}     {POT_USERNAME}          4096 May 21 14:26 .
drwxr-xr-x    1 {POT_USERNAME}     {POT_USERNAME}          4096 May  9 18:42 ..\n"""
        elif workdir == f"/home/{POT_USERNAME}/Desktop":
            response = f"""total 8
drwxr-xr-x    1 {POT_USERNAME}     {POT_USERNAME}          4096 May 21 14:26 .
drwxr-xr-x    1 {POT_USERNAME}     {POT_USERNAME}          4096 May  9 18:42 ..\n"""
        elif workdir == f"/home/{POT_USERNAME}/Documents":
            response = f"""total 8
drwxr-xr-x    1 {POT_USERNAME}     {POT_USERNAME}          4096 May 21 14:26 .
drwxr-xr-x    1 {POT_USERNAME}     {POT_USERNAME}          4096 May  9 18:42 ..\n"""
        elif workdir == f"/home/{POT_USERNAME}/Downloads":
            response = f"""total 8
drwxr-xr-x    1 {POT_USERNAME}     {POT_USERNAME}          4096 May 21 14:26 .
drwxr-xr-x    1 {POT_USERNAME}     {POT_USERNAME}          4096 May  9 18:42 ..\n"""
        elif workdir == f"/home/{POT_USERNAME}/Public":
            response = f"""total 8
drwxr-xr-x    1 {POT_USERNAME}     {POT_USERNAME}          4096 May 21 14:26 .
drwxr-xr-x    1 {POT_USERNAME}     {POT_USERNAME}          4096 May  9 18:42 ..\n"""
        elif workdir == f"/home/{POT_USERNAME}/Templates":
            response = f"""total 8
drwxr-xr-x    1 {POT_USERNAME}     {POT_USERNAME}          4096 May 21 14:26 .
drwxr-xr-x    1 {POT_USERNAME}     {POT_USERNAME}          4096 May  9 18:42 ..\n"""
        else:
            response = f"""total 8
drwxr-xr-x    1 {POT_USERNAME}     {POT_USERNAME}          4096 May 21 14:26 .
drwxr-xr-x    1 {POT_USERNAME}     {POT_USERNAME}          4096 May  9 18:42 ..\n"""
    else:   # ls <directory>
        change_dir_command = command.replace("ls", "cd", 1)
        _, new_cd_workdir = cd_command(
            change_dir_command, workdir, from_ls=True)
        response = ls_command("ls", new_cd_workdir)

    return response


def ps_command():
    response = f"""PID   USER     TIME  COMMAND
    1 {POT_USERNAME}      0:23 /bin/bash
   62 {POT_USERNAME}      0:00 ps\n"""
    return response


def pwd_command(workdir):
    response = f"""{workdir}\n"""
    return response


def whoami_command():
    response = f"""{POT_USERNAME}\n"""
    return response
