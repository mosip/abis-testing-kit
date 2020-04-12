from typing import List, Dict

import requests
from requests.auth import HTTPBasicAuth

from orchestrator.request_creator import create_identify_request, create_insert_request, create_delete_request, create_ping_request, create_reference_count_request
from config.settings_override import queue_config, app_config


def insert(request_id: str, reference_id: str):
    conf = queue_config()
    data = create_insert_request(request_id, reference_id)
    r = requests.post(conf.host + 'api/message/' + conf.send_address + '?type=queue', json=data,
                      auth=HTTPBasicAuth(conf.user, conf.password))
    if r.status_code == 200:
        return True, r.text, data
    else:
        return False, r.text, data


def identify(request_id: str, reference_id: str, gallery_reference_ids: List[str], config: Dict):
    conf = queue_config()
    data = create_identify_request(request_id, reference_id, app_config().callback_url+reference_id, gallery_reference_ids, config)
    r = requests.post(conf.host + 'api/message/' + conf.send_address + '?type=queue', json=data,
                      auth=HTTPBasicAuth(conf.user, conf.password))
    if r.status_code == 200:
        return True, r.text, data
    else:
        return False, r.text, data


def identify_ref(request_id: str, reference_id: str, gallery_reference_ids: List[str], config: Dict):
    conf = queue_config()
    data = create_identify_request(request_id, reference_id, "", gallery_reference_ids, config)
    r = requests.post(conf.host + 'api/message/' + conf.send_address + '?type=queue', json=data,
                      auth=HTTPBasicAuth(conf.user, conf.password))
    if r.status_code == 200:
        return True, r.text, data
    else:
        return False, r.text, data


def identify_url(request_id: str, reference_id: str, gallery_reference_ids: List[str], config: Dict):
    conf = queue_config()
    data = create_identify_request(request_id, "", app_config().callback_url+reference_id, gallery_reference_ids, config)
    r = requests.post(conf.host + 'api/message/' + conf.send_address + '?type=queue', json=data,
                      auth=HTTPBasicAuth(conf.user, conf.password))
    if r.status_code == 200:
        return True, r.text, data
    else:
        return False, r.text, data


def delete(request_id: str, reference_id: str):
    conf = queue_config()
    data = create_delete_request(request_id, reference_id)
    r = requests.post(conf.host + 'api/message/' + conf.send_address + '?type=queue', json=data,
                      auth=HTTPBasicAuth(conf.user, conf.password))
    if r.status_code == 200:
        return True, r.text, data
    else:
        return False, r.text, data


def ping(request_id: str):
    conf = queue_config()
    data = create_ping_request(request_id)
    r = requests.post(conf.host + 'api/message/' + conf.send_address + '?type=queue', json=data,
                      auth=HTTPBasicAuth(conf.user, conf.password))
    if r.status_code == 200:
        return True, r.text, data
    else:
        return False, r.text, data


def reference_count(request_id: str):
    conf = queue_config()
    data = create_reference_count_request(request_id)
    r = requests.post(conf.host + 'api/message/' + conf.send_address + '?type=queue', json=data,
                      auth=HTTPBasicAuth(conf.user, conf.password))
    if r.status_code == 200:
        return True, r.text, data
    else:
        return False, r.text, data
