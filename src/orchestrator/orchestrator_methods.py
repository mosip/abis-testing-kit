import json
import os
import re
from copy import deepcopy
from typing import Dict, List


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
        raise RuntimeError('Error is testcase. method not found')
    if method not in ['insert', 'identify', 'delete', 'ping', 'reference_count']:
        raise RuntimeError('Error is testcase. step: ' + st + ' is not a valid step')
    if parameters is None:
        raise RuntimeError('Error is testcase. step: no person info found. Step: ' + st)
    return method, parameters


def save(path: str, data):
    if os.path.isfile(path):
        os.remove(path)
    with open(path, "a") as mf:
        mf.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))
        mf.close()
