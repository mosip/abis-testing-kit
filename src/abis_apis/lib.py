"""
This utility provides helper functions related to ABIS APIs.
Check the docs to know about ABIS APIs
"""
import json
import time
import errno
import os
from typing import List
from config.settings import AppConfig


def insert(request_id: str, reference_id: str):
    """ Create a insert request

        Keyword arguments:
        request_id -- request_id
        reference_id -- reference_id
    """
    file_path = "config/insert.json"
    abs_file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', file_path))
    print("Absolute path of " + file_path + ": " + abs_file_path)
    if os.path.isfile(abs_file_path):
        with open(abs_file_path, 'r') as file:
            data = file.read()
            data = data.replace('${requestId}', request_id)
            data = data.replace('${referenceId}', reference_id)
            data = data.replace('${referenceURL}', AppConfig.callback_url)
            data = data.replace('${timestamp}', str(int(time.time())))
            return json.loads(data)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)


def identify(request_id: str, reference_id: str, reference_url: str, gallery_reference_ids: List[str]):
    """ Create a identify request

        Keyword arguments:
        request_id -- request_id
        reference_id -- reference_id
        reference_url -- reference_url
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
            data = data.replace('${timestamp}', str(int(time.time())))
            data = data.replace('${maxResults}', AppConfig.abis_max_results)
            data = data.replace('${targetFPIR}', AppConfig.abis_target_fpir)
            data = json.loads(data)
            if len(gallery_reference_ids) != 0:
                data["gallery"] = {"referenceIds": []}
                ph_gallery_reference_ids = []
                for gallery_reference_id in gallery_reference_ids:
                    data["gallery"]["referenceIds"].append({"referenceId": gallery_reference_id})

            return data
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)


def delete(request_id: str, reference_id: str):
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
            data = data.replace('${timestamp}', str(int(time.time())))
            return json.loads(data)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)


def ping(request_id: str):
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
            data = data.replace('${timestamp}', str(int(time.time())))
            return json.loads(data)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)


def reference_count(request_id: str):
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
            data = data.replace('${timestamp}', str(int(time.time())))
            return json.loads(data)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)