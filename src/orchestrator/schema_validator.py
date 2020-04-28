import errno
import json
import os
from typing import Any, Dict
from jsonschema import validate, ValidationError

abs_file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', 'config/schemas'))


def validate_insert_response(instance: Dict):
    schema_path = os.path.join(abs_file_path, 'insert_response.json')
    if os.path.isfile(schema_path):
        with open(schema_path, 'r') as file:
            schema = json.loads(file.read())
            try:
                validate(instance, schema)
                return True, ''
            except ValidationError as e:
                return False, "validate_insert_response :"+str(e)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), schema_path)


def validate_identify_response(instance: Dict):
    schema_path = os.path.join(abs_file_path, 'identify_response.json')
    if os.path.isfile(schema_path):
        with open(schema_path, 'r') as file:
            schema = json.loads(file.read())
            try:
                validate(instance, schema)
                return True, ''
            except ValidationError as e:
                return False, "validate_identify_response :"+str(e)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), schema_path)


def validate_delete_response(instance: Dict):
    schema_path = os.path.join(abs_file_path, 'delete_response.json')
    if os.path.isfile(schema_path):
        with open(schema_path, 'r') as file:
            schema = json.loads(file.read())
            try:
                validate(instance, schema)
                return True, ''
            except ValidationError as e:
                return False, "validate_delete_response :"+str(e)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), schema_path)


def validate_ping_response(instance: Dict):
    schema_path = os.path.join(abs_file_path, 'ping_response.json')
    if os.path.isfile(schema_path):
        with open(schema_path, 'r') as file:
            schema = json.loads(file.read())
            try:
                validate(instance, schema)
                return True, ''
            except ValidationError as e:
                return False, "validate_ping_response :"+str(e)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), schema_path)


def validate_pending_jobs_response(instance: Dict):
    schema_path = os.path.join(abs_file_path, 'pending_jobs_response.json')
    if os.path.isfile(schema_path):
        with open(schema_path, 'r') as file:
            schema = json.loads(file.read())
            try:
                validate(instance, schema)
                return True, ''
            except ValidationError as e:
                return False, "validate_pending_jobs_response :"+str(e)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), schema_path)


def validate_reference_count_response(instance: Dict):
    schema_path = os.path.join(abs_file_path, 'reference_count_response.json')
    if os.path.isfile(schema_path):
        with open(schema_path, 'r') as file:
            schema = json.loads(file.read())
            try:
                validate(instance, schema)
                return True, ''
            except ValidationError as e:
                return False, "validate_reference_count_response :"+str(e)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), schema_path)
