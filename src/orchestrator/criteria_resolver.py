from copy import deepcopy
from typing import Dict, List


def criteria_resolver(test_cases: List):
    final_results = []
    test_cases_c = deepcopy(test_cases)
    for test in test_cases_c:
        final_results.append(analyse(test))
    return final_results


def analyse(test: Dict):
    results = {"steps_failed": 0, "step_passed": 0}
    steps: List = test['steps']
    for step in test['steps']:
        if int(step['response']['returnValue']) == 1:
            results['step_passed'] += 1
        else:
            results['steps_failed'] += 1
    test['results'] = results
    return test



