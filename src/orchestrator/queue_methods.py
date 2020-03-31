import requests
from requests.auth import HTTPBasicAuth
from config.settings import Queue


def produce(queue, msg):
    r = requests.post(Queue.host+'api/message/' + queue + '?type=queue', json=msg,
                      auth=HTTPBasicAuth(Queue.user, Queue.password))
    if r.status_code == 200:
        return True, r.text
    else:
        return False, r.text


def consume(queue, client_id):
    r = requests.get(Queue.host+'api/message/' + queue + '?type=queue&clientId='+client_id, auth=HTTPBasicAuth(Queue.user, Queue.password))
    if r.status_code == 200:
        return True, r.json()
    else:
        return False, r.text