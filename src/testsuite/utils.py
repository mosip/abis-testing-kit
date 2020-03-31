import requests
import base64
from requests.auth import HTTPBasicAuth
from config.settings import CBEFFConfig, Queue
from cbeff import Biometrics


def produce(msg):
    r = requests.post(Queue.host + 'api/message/' + Queue.name + '?type=queue', json=msg,
                      auth=HTTPBasicAuth(Queue.user, Queue.password))
    if r.status_code == 200:
        return True, r.text
    else:
        return False, r.text


def consume():
    r = requests.get(Queue.host + 'api/message/' + Queue.name + '?type=queue&clientId='+Queue.client_id, auth=HTTPBasicAuth(Queue.user, Queue.password))
    if r.status_code == 200:
        return True, r.json()
    else:
        return False, r.text


def parse_biometric_file(name: str, path: str):
    strs = name.split('.')[0].split('_')
    if not name.endswith('.jpeg'):
        return False, None, "only jpeg format is allowed"
    if len(strs) != 2:
        return False, None, "filename should be <Biometric type>_<Biometric subtype>"

    with open(path, 'rb') as file:
        data = file.read()
        data = base64.b64encode(data).decode('utf-8')
        print("-----------------------------------------------------------------------------------------")
        print(type(data))
    biometric = Biometrics(strs[0], strs[1], data)
    return True, biometric, None

