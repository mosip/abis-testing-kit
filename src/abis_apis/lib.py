"""
This utility provides helper functions related to ABIS APIs.
Check the docs to know about ABIS APIs
"""
import json
import time
import errno
import os
from typing import List


def insert(request_id: str, reference_id: str, reference_url: str):
    """Create a insert request

        Keyword arguments:
        request_id -- request_id
        reference_id -- reference_id
        reference_url -- reference_url
    """
    file_path = "config/insert.json"
    abs_file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', file_path))
    print("Absolute path of "+file_path+": "+abs_file_path)
    if os.path.isfile(abs_file_path):
        with open(abs_file_path, 'r') as file:
            data = file.read()
            data = data.replace('${requestId}', request_id)
            data = data.replace('${referenceId}', reference_id)
            data = data.replace('${referenceURL}', reference_url)
            data = data.replace('${timestamp}', str(int(time.time())))
            return json.loads(data)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)


def identify(request_id: str, reference_id: str, reference_url: str, max_results: int, target_fpir: int, reference_ids: List[dict]):
    """Delete a CBEFF xml file

        Keyword arguments:
        path -- path of the file to be deleted
    """
    return


def delete(request_id: str, reference_id: str):
    """Validate a CBEFF xml file and return true (if valid)/ false (if invalid)

        Keyword arguments:
        path -- path of the file to be validated
    """
    return
