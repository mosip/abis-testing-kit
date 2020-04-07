import errno
import json
import os
import re
from copy import deepcopy
from typing import Dict, List
from jsonschema import validate, ValidationError

abs_file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', 'config/schemas'))


def validate_test_cases(tcs: List):
    schema_path = os.path.join(abs_file_path, 'testcase.schema.json')
    if os.path.isfile(schema_path):
        with open(schema_path, 'r') as file:
            schema = json.loads(file.read())
            try:
                validate(tcs, schema)
                return True
            except ValidationError as e:
                raise NameError("Test case file is incorrect: "+str(e))
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), schema_path)


def validate_test_data(data: List):
    schema_path = os.path.join(abs_file_path, 'testdata.schema.json')
    if os.path.isfile(schema_path):
        with open(schema_path, 'r') as file:
            schema = json.loads(file.read())
            try:
                validate(data, schema)
                return True
            except ValidationError as e:
                raise NameError("Test data file is incorrect: "+str(e))
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), schema_path)


def parse_test_cases(tcs: List):
    ptcs = deepcopy(tcs)
    for tc_key, tc in enumerate(tcs):
        ptcs[tc_key]['steps'] = []
        for st in tc['steps']:
            method, parameters = parse_step(st)
            ptcs[tc_key]['steps'].append({'method': method, 'parameters': parameters})
    return ptcs


def parse_step(st: str):
    parameters = None
    method = None
    m = re.search('([a-zA-Z_]*)\\(', st)
    if m:
        method = m.group(1)
    p = re.search('\\((.*)\\)', st)
    if p:
        found = p.group(1)
        parameters = [i.strip(' ') for i in found.split(',')]
    if method is None:
        raise RuntimeError('orchestrator_methods: Error is testcase. method not found')
    if method not in ['insert', 'identify', 'identify_url', 'delete', 'ping', 'reference_count']:
        raise RuntimeError('orchestrator_methods: Error is testcase. step: ' + st + ' is not a valid step')
    if parameters is None:
        raise RuntimeError('orchestrator_methods: Error is testcase. step: no person info found. Step: ' + st)
    return method, parameters


def save_file(path: str, data):
    if os.path.isfile(path):
        os.remove(path)
    with open(path, "a") as mf:
        mf.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))
        mf.close()



