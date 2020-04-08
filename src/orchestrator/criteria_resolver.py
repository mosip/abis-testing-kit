from copy import deepcopy
from typing import Dict, List
from orchestrator.schema_validator import validate_insert_response, validate_identify_response, validate_delete_response, validate_ping_response, validate_reference_count_response


def criteria_resolver(test_cases: List):
    final_results = []
    test_cases_c = deepcopy(test_cases)
    for test in test_cases_c:
        test['runResults'] = {}
        final_results.append(analyse(response_validator(test)))
    return final_results


def analyse(test: Dict):
    failed = 0
    passed = 0
    steps: List = test['steps']
    for idx, step in enumerate(test['steps']):
        if step['passed'] is True:
            if int(step['response']['returnValue']) == 1:
                failed += 1
                test['steps'][idx]['passed'] = False
            else:
                passed += 1
                test['steps'][idx]['passed'] = True
        else:
            failed += 1
            test['steps'][idx]['passed'] = False
    test['runResults']['failed'] = failed
    test['runResults']['passed'] = passed
    return test


def response_validator(test: Dict):
    steps: List = test['steps']
    for idx, step in enumerate(test['steps']):
        test['steps'][idx]['response_validation'] = {}
        if step['method'] == 'insert':
            status, msg = validate_insert_response(step['response'])
        elif step['method'] == 'identify':
            status, msg = validate_identify_response(step['response'])
        elif step['method'] == 'identify_url':
            status, msg = validate_identify_response(step['response'])
        elif step['method'] == 'delete':
            status, msg = validate_delete_response(step['response'])
        elif step['method'] == 'ping':
            status, msg = validate_ping_response(step['response'])
        elif step['method'] == 'reference_count':
            status, msg = validate_reference_count_response(step['response'])
        else:
            status = False
            msg = "Step validation not found"

        if status is True:
            test['steps'][idx]['response_validation']['passed'] = True
            test['steps'][idx]['passed'] = True
        else:
            test['steps'][idx]['response_validation']['passed'] = False
            test['steps'][idx]['response_validation']['msg'] = msg
            test['steps'][idx]['passed'] = False

    return test



