from copy import deepcopy
from typing import Dict, List

from config.settings_override import app_config
from orchestrator.schema_validator import validate_insert_response, validate_identify_response, \
    validate_delete_response, validate_ping_response, validate_pending_jobs_response, validate_reference_count_response


def criteria_resolver(test_cases: List, store: Dict):
    final_results = []
    test_cases_c = deepcopy(test_cases)
    for test in test_cases_c:
        test['testResults'] = {}
        final_results.append(analyse(response_validator(test), store))
    return final_results


def analyse(test: Dict, store: Dict):
    failed = 0
    analysis = []
    identify_exps = ['candidateListCount', 'candidateReferenceId']
    steps: List = test['steps']
    for idx, step in enumerate(test['steps']):
        step_failed = False
        test['steps'][idx]['passed'] = True
        if step['passed'] is True:
            if len(step['expectations']) > 0:
                for aexp in step['expectations']:
                    if aexp['type'] in identify_exps or aexp['type'] in ('!'+s for s in identify_exps):
                        status, msg = identify_criteria_resolver(aexp, step['response'], store)
                        if status is False:
                            failed += 1
                            test['steps'][idx]['passed'] = False
                            analysis.append('Step #' + str(idx + 1) + ' ' + msg)
                            break
                    else:
                        status, msg = common_criteria_resolver(aexp, step['response'])
                        if status is False:
                            failed += 1
                            test['steps'][idx]['passed'] = False
                            analysis.append('Step #' + str(idx + 1) + ' ' + msg)
                            break
            else:
                if int(step['response']['returnValue']) != 1:
                    failed += 1
                    test['steps'][idx]['passed'] = False
                    analysis.append('Step #' + str(idx + 1) + ' failed: Expected returnValue [1], actual [' + str(
                        step['response']['returnValue']) + ']')
        else:
            failed += 1
            test['steps'][idx]['passed'] = False
            analysis.append('Step #' + str(idx + 1) + ' failed: structure validation failed')

    if failed == 0:
        test['testResults']['status'] = 'passed'
    else:
        test['testResults']['status'] = 'failed'
    test['testResults']['reasonsForFailure'] = analysis
    return test


def common_criteria_resolver(expect: Dict, response: Dict):
    try:
        passed = True
        msg = ""
        etype = expect['type'].replace("!", "")
        evalue = expect['value']
        if etype not in response:
            passed = False
            msg = 'Response does not contain ' + etype
            return passed, msg
        if "!" in expect['type']:
            if str(response[etype]) == evalue:
                passed = False
                msg = 'Expected ' + etype + ' [not ' + evalue + '], actual [' + str(response[etype]) + ']'
                return passed, msg
        else:
            if str(response[etype]) != evalue:
                passed = False
                msg = 'Expected ' + etype + ' [' + evalue + '], actual [' + str(response[etype]) + ']'
                return passed, msg
        return passed, msg
    except Exception as e:
        print("OS error: {0}".format(e))
        raise Exception("common_criteria_resolver: "+str(e))


def identify_criteria_resolver(expect: Dict, response: Dict, store: Dict):
    try:
        passed = True
        msg = ""
        etype = expect['type'].replace("!", "")
        evalue = expect['value']
        app_conf = app_config()
        if etype == 'candidateListCount' or etype == '!candidateListCount':
            if "candidateList" not in response:
                passed = False
                msg = 'Response does not contain candidateList'
                return passed, msg
            if "count" not in response['candidateList']:
                passed = False
                msg = 'Response does not contain count in candidateList object'
                return passed, msg
            if "!" in expect['type']:
                if str(response['candidateList']['count']) == evalue:
                    passed = False
                    msg = 'Expected candidateList->count [not ' + evalue + '], actual [' + str(response['candidateList']['count']) + ']'
                    return passed, msg
            else:
                if str(response['candidateList']['count']) != evalue:
                    passed = False
                    msg = 'Expected candidateList->count [' + evalue + '], actual [' + str(response['candidateList']['count']) + ']'
                    return passed, msg

        if "candidateList" not in response and "count" in response['candidateList'] and response['candidateList']['count'] > 0:
            for cands in response['candidateList']['candidates']:
                if int(cands['scaledScore']) < int(app_conf.abis_threshold):
                    passed = False
                    msg = 'Expected scaledScore [greater than '+app_conf.abis_threshold+'], actual ['+cands['scaledScore']+']'
                    return passed, msg

        if etype == 'candidateReferenceId' or etype == '!candidateReferenceId':
            cand_found = False
            if "candidateList" not in response and "count" in response['candidateList'] and response['candidateList']['count'] > 0:
                if evalue in store:
                    for cands in response['candidateList']['candidates']:
                        if cands['referenceId'] == store[evalue]['referenceId']:
                            cand_found = True
                    if cand_found is False:
                        passed = False
                        msg = 'Expected ['+store[evalue]['referenceId']+'] referenceId not not found in candidates info'
                        return passed, msg
                else:
                    passed = False
                    msg = 'persona data does not contain '+etype+'. Possible, you have make some mistake in testcase, persona data'
                    return passed, msg
        return passed, msg
    except Exception as e:
        print("OS error: {0}".format(e))
        raise Exception("identify_criteria_resolver: "+str(e))


def response_validator(test: Dict):
    try:
        steps: List = test['steps']
        for idx, step in enumerate(test['steps']):
            test['steps'][idx]['responseStructureValidation'] = {}
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
            elif step['method'] == 'pending_jobs':
                status, msg = validate_pending_jobs_response(step['response'])
            elif step['method'] == 'reference_count':
                status, msg = validate_reference_count_response(step['response'])
            else:
                status = False
                msg = "Step validation not found"

            if status is True:
                test['steps'][idx]['responseStructureValidation']['passed'] = 'passed'
                test['steps'][idx]['responseStructureValidation']['msg'] = 'validation passed'
                test['steps'][idx]['passed'] = True
            else:
                test['steps'][idx]['responseStructureValidation']['passed'] = 'failed'
                test['steps'][idx]['responseStructureValidation']['msg'] = msg
                test['steps'][idx]['passed'] = False

        return test
    except Exception as e:
        print("response_validator: ".format(e))
        raise Exception("response_validator: "+str(e))
