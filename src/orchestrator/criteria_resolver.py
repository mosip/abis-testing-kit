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
    analysis = []
    steps: List = test['steps']
    for idx, step in enumerate(test['steps']):
        if len(step['asserts']) > 0:
            for asrt in step['asserts']:
                if asrt['type'] == 'returnValue':
                    if str(step['response']['returnValue']) != asrt['value']:
                        failed += 1
                        test['steps'][idx]['passed'] = False
                        analysis.append('Step #'+str(idx+1)+' failed: Expected '+asrt['type']+' ['+asrt['value']+'], actual ['+str(step['response']['returnValue'])+']')
                        break
                elif asrt['type'] == 'count':
                    if "count" not in step['response']:
                        failed += 1
                        test['steps'][idx]['passed'] = False
                        analysis.append('Step #' + str(idx + 1) + ' failed: Response does not contain '+asrt['type'])
                        break
                    if str(step['response']['count']) != asrt['value']:
                        failed += 1
                        test['steps'][idx]['passed'] = False
                        analysis.append('Step #'+str(idx+1)+' failed: Expected '+asrt['type']+' ['+asrt['value']+'], actual ['+str(step['response']['count'])+']')
                        break
                elif asrt['type'] == 'jobscount':
                    if "count" not in step['response']:
                        failed += 1
                        test['steps'][idx]['passed'] = False
                        analysis.append('Step #' + str(idx + 1) + ' failed: Response does not contain '+asrt['type'])
                        break
                    if str(step['response']['jobscount']) != asrt['value']:
                        failed += 1
                        test['steps'][idx]['passed'] = False
                        analysis.append('Step #'+str(idx+1)+' failed: Expected '+asrt['type']+' ['+asrt['value']+'], actual ['+str(step['response']['jobscount'])+']')
                        break
                elif asrt['type'] == 'candidates':
                    if "candidateList" not in step['response']:
                        failed += 1
                        test['steps'][idx]['passed'] = False
                        analysis.append('Step #' + str(idx + 1) + ' failed: Response does not contain candidateList')
                        break
                    if str(step['response']['candidateList']['count']) != asrt['value']:
                        failed += 1
                        test['steps'][idx]['passed'] = False
                        analysis.append('Step #'+str(idx+1)+' failed: Expected '+asrt['type']+' ['+asrt['value']+'], actual ['+str(step['response']['candidateList']['count'])+']')
                        break
        else:
            if step['passed'] is True:
                if int(step['response']['returnValue']) != 1:
                    failed += 1
                    test['steps'][idx]['passed'] = False
                    analysis.append('Step #' + str(idx + 1) + ' failed: Expected returnValue [1], actual [' + str(step['response']['returnValue']) + ']')
                else:
                    passed += 1
                    test['steps'][idx]['passed'] = True
            else:
                failed += 1
                test['steps'][idx]['passed'] = False
                analysis.append('Step #' + str(idx + 1) + ' failed: Expected returnValue [1], actual [' + str(step['response']['returnValue']) + ']')
    test['runResults']['failed'] = failed
    test['runResults']['passed'] = passed
    test['runResults']['analysis'] = analysis
    return test


def response_validator(test: Dict):
    steps: List = test['steps']
    for idx, step in enumerate(test['steps']):
        test['steps'][idx]['structure_validation'] = {}
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
            test['steps'][idx]['structure_validation']['passed'] = 'passed'
            test['steps'][idx]['structure_validation']['msg'] = 'validation passed'
            test['steps'][idx]['passed'] = True
        else:
            test['steps'][idx]['structure_validation']['passed'] = 'failed'
            test['steps'][idx]['structure_validation']['msg'] = msg
            test['steps'][idx]['passed'] = False

    return test



