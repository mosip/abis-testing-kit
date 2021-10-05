import datetime
import errno
import json
import os
import re
import shutil
import zipfile
from copy import deepcopy
from typing import List, Dict
from jsonschema import validate, ValidationError

abs_tmp_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../../', 'tmp'))
abs_store_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', 'store'))
abs_schema_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', 'config/schemas'))


def extract_testdata(path: str):
    archive = zipfile.ZipFile(path, 'r')
    archive.extractall(os.path.join(path, './../', 'testdata'))

    test_case_file_path = os.path.join(abs_tmp_path, 'testdata', 'test_cases.json')
    persona_data_file_path = os.path.join(abs_tmp_path, 'testdata', 'persona_data.json')
    if not os.path.isfile(test_case_file_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), test_case_file_path)
    if not os.path.isfile(persona_data_file_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), persona_data_file_path)

    with open(test_case_file_path, 'r') as file:
        test_cases: List = json.loads(file.read())
        validate_test_cases(test_cases)
        parse_test_cases(test_cases)

    with open(persona_data_file_path, 'r') as file:
        test_data: List = json.loads(file.read())
        validate_test_data(test_data)

    """ remove store """
    for fl in os.listdir(abs_store_path):
        if not fl.endswith('.gitkeep'):
            os.remove(os.path.join(abs_store_path, fl))

    """ copy testdata files to store """
    for fs in os.listdir(os.path.join(abs_tmp_path, 'testdata')):
        if fs.endswith('.xml') or fs.endswith('.json'):
            shutil.copy(os.path.join(abs_tmp_path, 'testdata', fs), os.path.join(abs_store_path, fs))


def validate_test_cases(tcs: List):
    schema_path = os.path.join(abs_schema_path, 'testcase.schema.json')
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
    schema_path = os.path.join(abs_schema_path, 'personadata.schema.json')
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
        for idx, st in enumerate(tc['steps']):
            try:
                p_step = parse_step(st)
                p_step['stepId'] = str(idx+1)
            except Exception as e:
                raise RuntimeError('Error while parsing step: '+st+' of testcase: '+tc['testId']+'. More info --- '+str(e))
            ptcs[tc_key]['steps'].append(p_step)
    return ptcs


def parse_step(st: str):
    allowed_methods = ['insert', 'identify', 'identify_ref', 'identify_url', 'delete', 'ping', 'pending_jobs', 'reference_count']
    step = {"method": None, "parameters": [], "expectations": []}
    expectations = ['returnValue', 'failureReason', 'count', 'jobscount', 'candidateListCount', 'candidateReferenceId']
    parameters = None
    method = None
    sts = st.split(".")
    for idx, mstr in enumerate(sts):
        if idx == 0:
            m = re.search('([a-zA-Z_]*)\\(', mstr)
            if m:
                method = m.group(1)
            p = re.search('\\((.*)\\)', mstr)
            if p:
                found = p.group(1)
                parameters = [i.strip(' ') for i in found.split(',')]
            if method is None:
                raise RuntimeError('orchestrator_methods: method not found.')
            if method not in allowed_methods:
                raise RuntimeError('orchestrator_methods: step: ' + st + ' is not a valid step')
            if parameters is None:
                raise RuntimeError('orchestrator_methods: step: no person info found.')
            step["method"] = method
            step["parameters"] = parameters
        else:
            m = re.findall('((?i)expect)\\(.*\\)', mstr)
            if len(m) == 1:
                p = re.findall('\\((.*)\\)', mstr)
                if len(p) == 1:
                    found = p[0]
                    value = [i.strip(' ') for i in found.split(',')]
                    if len(value) != 2:
                        raise RuntimeError('orchestrator_methods: expect must have a type and value.')
                    a_type = value[0]
                    if a_type not in expectations and a_type not in ('!'+s for s in expectations):
                        raise RuntimeError('orchestrator_methods: : expectations type can only be '+''.join(expectations)+' or '+''.join(('!'+s for s in expectations)))
                    exp = {"type": a_type, "value": value[1]}
                    step["expectations"].append(exp)
                else:
                    raise RuntimeError('orchestrator_methods: Error in step syntax : ' + mstr)
            else:
                raise RuntimeError('orchestrator_methods: Error in step syntax : ' + mstr)
    return step


def save_file(path: str, data):
    if os.path.isfile(path):
        os.remove(path)
    with open(path, "a") as mf:
        mf.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))
        mf.close()


def create_zip(path: str, dest: str):
    zipf = zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.json') or file.endswith('.xml'):
                zipf.write(os.path.join(root, file), file)
    zipf.close()


def cleanTmp():
    if os.path.exists(abs_tmp_path):
        for root, dirs, files in os.walk(abs_tmp_path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))


def getTime():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")