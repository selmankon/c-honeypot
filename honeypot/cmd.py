import subprocess


def run_command(command):
    try:
        output = subprocess.check_output(
            command, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        output = e.output
    return output
