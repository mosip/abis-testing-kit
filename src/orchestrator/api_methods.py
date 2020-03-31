from typing import List

import requests
from requests.auth import HTTPBasicAuth

from abis_apis import prepare_insert_request, prepare_identify_request, prepare_delete_request, prepare_ping_request, prepare_reference_count_request
from config.settings import Queue


def insert(request_id: str, reference_id: str):
    data = prepare_insert_request(request_id, reference_id)
    r = requests.post(Queue.host + 'api/message/' + Queue.send_address + '?type=queue', json=data,
                      auth=HTTPBasicAuth(Queue.user, Queue.password))
    if r.status_code == 200:
        return True, r.text, data
    else:
        return False, r.text, data


def identify(request_id: str, reference_id: str, gallery_reference_ids: List[str]):
    data = prepare_identify_request(request_id, reference_id, gallery_reference_ids)
    r = requests.post(Queue.host + 'api/message/' + Queue.send_address + '?type=queue', json=data,
                      auth=HTTPBasicAuth(Queue.user, Queue.password))
    if r.status_code == 200:
        return True, r.text, data
    else:
        return False, r.text, data


def delete(request_id: str, reference_id: str):
    data = prepare_delete_request(request_id, reference_id)
    r = requests.post(Queue.host + 'api/message/' + Queue.send_address + '?type=queue', json=data,
                      auth=HTTPBasicAuth(Queue.user, Queue.password))
    if r.status_code == 200:
        return True, r.text, data
    else:
        return False, r.text, data


def ping(request_id: str):
    data = prepare_ping_request(request_id)
    r = requests.post(Queue.host + 'api/message/' + Queue.send_address + '?type=queue', json=data,
                      auth=HTTPBasicAuth(Queue.user, Queue.password))
    if r.status_code == 200:
        return True, r.text, data
    else:
        return False, r.text, data


def reference_count(request_id: str):
    data = prepare_reference_count_request(request_id)
    r = requests.post(Queue.host + 'api/message/' + Queue.send_address + '?type=queue', json=data,
                      auth=HTTPBasicAuth(Queue.user, Queue.password))
    if r.status_code == 200:
        return True, r.text, data
    else:
        return False, r.text, data
