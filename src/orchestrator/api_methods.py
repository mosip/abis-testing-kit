from typing import List

import requests
from requests.auth import HTTPBasicAuth

from orchestrator.request_creator import create_identify_request, create_insert_request, create_delete_request, create_ping_request, create_reference_count_request
from config.settings import Queue, AppConfig


def insert(request_id: str, reference_id: str):
    data = create_insert_request(request_id, reference_id)
    r = requests.post(Queue.host + 'api/message/' + Queue.send_address + '?type=queue', json=data,
                      auth=HTTPBasicAuth(Queue.user, Queue.password))
    if r.status_code == 200:
        return True, r.text, data
    else:
        return False, r.text, data


def identify(request_id: str, reference_id: str, gallery_reference_ids: List[str]):
    data = create_identify_request(request_id, reference_id, "", gallery_reference_ids)
    r = requests.post(Queue.host + 'api/message/' + Queue.send_address + '?type=queue', json=data,
                      auth=HTTPBasicAuth(Queue.user, Queue.password))
    if r.status_code == 200:
        return True, r.text, data
    else:
        return False, r.text, data


def identify_url(request_id: str, reference_id: str, gallery_reference_ids: List[str]):
    data = create_identify_request(request_id, "", AppConfig.callback_url+reference_id, gallery_reference_ids)
    r = requests.post(Queue.host + 'api/message/' + Queue.send_address + '?type=queue', json=data,
                      auth=HTTPBasicAuth(Queue.user, Queue.password))
    if r.status_code == 200:
        return True, r.text, data
    else:
        return False, r.text, data


def delete(request_id: str, reference_id: str):
    data = create_delete_request(request_id, reference_id)
    r = requests.post(Queue.host + 'api/message/' + Queue.send_address + '?type=queue', json=data,
                      auth=HTTPBasicAuth(Queue.user, Queue.password))
    if r.status_code == 200:
        return True, r.text, data
    else:
        return False, r.text, data


def ping(request_id: str):
    data = create_ping_request(request_id)
    r = requests.post(Queue.host + 'api/message/' + Queue.send_address + '?type=queue', json=data,
                      auth=HTTPBasicAuth(Queue.user, Queue.password))
    if r.status_code == 200:
        return True, r.text, data
    else:
        return False, r.text, data


def reference_count(request_id: str):
    data = create_reference_count_request(request_id)
    r = requests.post(Queue.host + 'api/message/' + Queue.send_address + '?type=queue', json=data,
                      auth=HTTPBasicAuth(Queue.user, Queue.password))
    if r.status_code == 200:
        return True, r.text, data
    else:
        return False, r.text, data
