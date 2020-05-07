## How to write test cases

A test case json file contains an array of test object that contains the necessary to run tests

* testId can be a unique identifier for a test
* testDescription, description of the test
* steps, a list of function to execute with the persona name in "()"

### Steps

**insert(persona)**

* sends an insert request to the queue with the reference id of the persona. 
* callback url will be sent in request from which the ABIS will fetch cbeff associated with the persona

[know more about request](https://mosipdocs.gitbook.io/platform/functionalities/apis/abis-apis#insert)

**identify(persona_1, persona_2, persona_3,..,...)**

* sends an identify request to the queue with the reference id of person_1
* gallery of reference ids of persona_2, persona_3,...
* if only persona_1 is provided, then it will send no gallery and the match will happen with all inserted data

[know more about request](https://mosipdocs.gitbook.io/platform/functionalities/apis/abis-apis#identify)

**delete(persona_1)**

* sends an delete request to the queue with the reference id of person_1

[know more about request](https://mosipdocs.gitbook.io/platform/functionalities/apis/abis-apis#delete)

**ping**

* sends an ping request to the queue to get service status

[know more about request](https://mosipdocs.gitbook.io/platform/functionalities/apis/abis-apis#ping)

**pending_jobs**

* sends pending_jobs request to the queue to get pending Jobs count

[know more about request](https://mosipdocs.gitbook.io/platform/functionalities/apis/abis-apis#pending-jobs)

**reference_count**

* sends an reference_count request to the queue

[know more about request](https://mosipdocs.gitbook.io/platform/functionalities/apis/abis-apis#reference-count)

### Expectations:
You can add expectation to a step by adding "expect(<type>, <value>)"

type can be:
* returnValue (applicable on all steps)
* failureReason (applicable on all steps)
* count (applicable only for ping)
* jobscount (applicable only for reference_count)
* candidateListCount (applicable only for identify, identify_url)
* candidateReferenceId (applicable only for identify, identify_url)

value is the expected value. 

**returnValue**

Matches for the returnValue field's value in response with expected value.

Example: expect(returnValue, 1)

**failureReason**

Matches for the failureReason field's value in response with expected value.

Example: expect(failureReason, 7)

**count**

Matches for the count field's value in response with expected value

Example: expect(count, 10)

**jobscount**

Matches for the jobscount field's value in response with expected value

Example: expect(jobscount, 10)

**candidateListCount**

Matches for the candidateList->count field's value in response with expected value.

Example: expect(candidateListCount, 2)

**candidateReferenceId**

Matches for the candidates reference_id field's value in response with expected value.

Example: expect(candidateReferenceId, person1)

**For example** 

.expect(returnValue, 2) - response.returnValue == 2, expected [2] & actual [response.returnValue]
.expect(!returnValue, 2) - response.returnValue != 2, expected [not 2] & actual [response.returnValue]

Orchestrator will check whether the expect condition is fulfilled, if not then it will set the status as failed

_* By default every step has an inbuilt expectation of returnValue 1. But if you add any expectation then you have to explicitly write the returnValue expect too_

### Example

```json
[
    {
        "testId": "x1",
        "testDescription": "y1",
        "steps": [
            "insert(person1)", "insert(person2)", "identify(person3, person1, person2).expect(returnValue, 1).expect(candidates, 2)"
        ]
    },
    {
        "testId": "x2",
        "testDescription": "y2",
        "steps": [
            "insert(person1)", "insert(person2)", "ping().expect(returnValue, 1).expect(jobscount, 2)"
        ]
    }
]
```