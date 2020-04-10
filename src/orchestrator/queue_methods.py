from typing import Dict

import requests
from requests.auth import HTTPBasicAuth


def produce(msg: Dict, host: str, queue: str, user: str, password: str):
    r = requests.post(host + 'api/message/' + queue + '?type=queue', json=msg,
                      auth=HTTPBasicAuth(user, password))
    if r.status_code == 200:
        return True, r.text
    else:
        return False, r.text


def consume(host: str, queue: str, user: str, password: str, client_id: str):
    r = requests.get(host + 'api/message/' + queue + '?type=queue&clientId=' + client_id,
                     auth=HTTPBasicAuth(user, password))
    if r.status_code == 200:
        return True, r.json()
    else:
        return False, r.text
