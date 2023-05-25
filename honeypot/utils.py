from settings import POT_USERNAME, PANEL_ENDPOINT
import requests
from datetime import datetime


def del_home_workdir(workdir):
    if workdir.startswith(f"/home/{POT_USERNAME}"):
        return workdir.replace(f"/home/{POT_USERNAME}", "~")
    return workdir


def send_to_api(cmd, ip_port):
    ip_port = f"{ip_port[0]}:{ip_port[1]}"
    timestamp_obj = datetime.now()
    timestamp = timestamp_obj.strftime("%d/%b/%Y %H:%M:%S")
    try:
        r = requests.post(PANEL_ENDPOINT, json={
            "command": cmd,
            "ip_port": ip_port,
            "timestand": timestamp,
            "level": 1,
            "source": 'Telnet',
        })
    except Exception as e:
        print(f"Unable to send data to API. {e}")
        return False, e

    return True, None
