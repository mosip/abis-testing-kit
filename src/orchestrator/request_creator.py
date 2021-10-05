"""
This utility provides helper functions related to ABIS APIs.
Check the docs to know about ABIS APIs
"""
import json
import errno
import os
from typing import List, Dict
from config.settings_override import app_config
from orchestrator.orchestrator_methods import getTime


def create_insert_request(request_id: str, reference_id: str):
    """ Create a insert request

        Keyword arguments:
        request_id -- request_id
        reference_id -- reference_id
    """
    app_conf = app_config()
    file_path = "config/insert.json"
    abs_file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', file_path))
    print("Absolute path of " + file_path + ": " + abs_file_path)
    if os.path.isfile(abs_file_path):
        with open(abs_file_path, 'r') as file:
            data = file.read()
            data = data.replace('${requestId}', request_id)
            data = data.replace('${referenceId}', reference_id)
            data = data.replace('${referenceURL}',  app_config().callback_url+reference_id)
            data = data.replace('${requesttime}', str(getTime()))
            return json.loads(data)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)


def create_identify_request(request_id: str, reference_id: str, reference_url: str, gallery_reference_ids: List[str], flags: Dict):
    """ Create a identify request

        Keyword arguments:
        request_id -- request_id
        reference_id -- reference_id
        gallery_reference_ids -- gallery reference ids to match with
    """
    file_path = "config/identify.json"
    abs_file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', file_path))
    print("Absolute path of " + file_path + ": " + abs_file_path)
    if os.path.isfile(abs_file_path):
        with open(abs_file_path, 'r') as file:
            data = file.read()
            data = data.replace('${requestId}', request_id)
            data = data.replace('${referenceId}', reference_id)
            data = data.replace('${referenceURL}', reference_url)
            data = data.replace('${requesttime}', str(getTime()))
            data = data.replace('"${flags}"', json.dumps(flags))
            data = json.loads(data)
            if len(gallery_reference_ids) != 0:
                data["gallery"] = {"referenceIds": []}
                for gallery_reference_id in gallery_reference_ids:
                    data["gallery"]["referenceIds"].append({"referenceId": gallery_reference_id})

            return data
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)


def create_delete_request(request_id: str, reference_id: str):
    """ Create a delete request

        Keyword arguments:
        request_id -- request_id
        reference_id -- reference_id
    """
    file_path = "config/delete.json"
    abs_file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', file_path))
    print("Absolute path of " + file_path + ": " + abs_file_path)
    if os.path.isfile(abs_file_path):
        with open(abs_file_path, 'r') as file:
            data = file.read()
            data = data.replace('${requestId}', request_id)
            data = data.replace('${referenceId}', reference_id)
            data = data.replace('${requesttime}', str(getTime()))
            return json.loads(data)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)


def create_ping_request(request_id: str):
    """ Create a ping request

        Keyword arguments:
        request_id -- request_id
    """
    file_path = "config/ping.json"
    abs_file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', file_path))
    print("Absolute path of " + file_path + ": " + abs_file_path)
    if os.path.isfile(abs_file_path):
        with open(abs_file_path, 'r') as file:
            data = file.read()
            data = data.replace('${requestId}', request_id)
            data = data.replace('${requesttime}', str(getTime()))
            return json.loads(data)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)


def create_pending_jobs_request(request_id: str):
    """ Create a ping request

        Keyword arguments:
        request_id -- request_id
    """
    file_path = "config/pending_jobs.json"
    abs_file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', file_path))
    print("Absolute path of " + file_path + ": " + abs_file_path)
    if os.path.isfile(abs_file_path):
        with open(abs_file_path, 'r') as file:
            data = file.read()
            data = data.replace('${requestId}', request_id)
            data = data.replace('${requesttime}', str(getTime()))
            return json.loads(data)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)


def create_reference_count_request(request_id: str):
    """ Create a reference count request

        Keyword arguments:
        request_id -- request_id
    """
    file_path = "config/reference_count.json"
    abs_file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', file_path))
    print("Absolute path of " + file_path + ": " + abs_file_path)
    if os.path.isfile(abs_file_path):
        with open(abs_file_path, 'r') as file:
            data = file.read()
            data = data.replace('${requestId}', request_id)
            data = data.replace('${requesttime}', str(getTime()))
            return json.loads(data)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)