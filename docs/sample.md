## Sample test

Results file contains brief information of the last test run, also the overall status of the test (pass/ fail)

### Example

**Test data file**

```json
[
    {
        "name": "person1",
        "reference_id": "r1"
    },
    {
        "name": "person2",
        "reference_id": "r2"
    },
    {
        "name": "person3",
        "reference_id": "r3"
    }
]
```

**Test case file**

```json
[
    {
        "testId": "test_unknown",
        "testDescription": "a sample test",
        "steps": [
            "insert(person1)", 
            "insert(person2)", 
            "identify(person3, person1, person2)", 
            "delete(person3)"
        ]
    }
]
```

**Results file of above test case (ideal scenario)**

```json
[
    {
        "testId": "test_unknown",
        "testDescription": "a sample test",
        "steps": [
            {
                "method": "insert",
                "parameters": [
                    "person1"
                ],
                "requestId": "<id of the request>",
                "requestStatus": "<status can be true/ false; true, if request is successful>",
                "requestMsg": "<msg received after sending request>",
                "request": {
                    "id": "mosip.abis.insert",
                    "ver": "1.0",
                    "requestId": "<id of the request>",
                    "timestamp": "<timestamp>",
                    "referenceId": "r1",
                    "referenceURL": "http://localhost:8000/get_cbeff/"
                },
                "response": {
                    "id": "mosip.abis.insert",
                    "requestId": "<id of the request>",
                    "timestamp": "<timestamp>",
                    "returnValue": 1
                },
                "responseStructureValidation": {
                    "passed": "<true/ false, true if the response of ABIS is structurally correct>",
                    "msg": "<some text to explain the reason>"
                },
                "passed": "<overall passed/ failed"
            },
            {
                "method": "insert",
                "parameters": [
                    "person2"
                ],
                "requestId": "<id of the request>",
                "requestStatus": "<status can be true/ false; true, if request is successful>",
                "requestMsg": "<msg received after sending request>",
                "request": {
                    "id": "mosip.abis.insert",
                    "ver": "1.0",
                    "requestId": "<id of the request>",
                    "timestamp": "<timestamp>",
                    "referenceId": "r2",
                    "referenceURL": "http://localhost:8000/get_cbeff/"
                },
                "response": {
                    "id": "mosip.abis.insert",
                    "requestId": "<id of the request>",
                    "timestamp": "<timestamp>",
                    "returnValue": 1
                },
                "responseStructureValidation": {
                    "passed": "<true/ false, true if the response of ABIS is structurally correct>",
                    "msg": "<some text to explain the reason>"
                },
                "passed": "<overall passed/ failed"
            },
            {
                "method": "identify",
                "parameters": [
                    "person3",
                    "person1",
                    "person2"
                ],
                "requestId": "<id of the request>",
                "requestStatus": "<status can be true/ false; true, if request is successful>",
                "requestMsg": "<msg received after sending request>",
                "request": {
                    "id": "mosip.abis.identify",
                    "ver": "1.0",
                    "requestId": "<id of the request>",
                    "timestamp": "<timestamp>",
                    "referenceId": "r3",
                    "referenceURL": "",
                    "maxResults": "30",
                    "targetFPIR": "30",
                    "gallery": {
                        "referenceIds": [
                            {
                                "referenceId": "r1"
                            },
                            {
                                "referenceId": "r2"
                            }
                        ]
                    }
                },
                "response": {
                    "id": "mosip.abis.identify",
                    "requestId": "<id of the request>",
                    "timestamp": "<timestamp>",
                    "returnValue": 1
                },
                "responseStructureValidation": {
                    "passed": "<true/ false, true if the response of ABIS is structurally correct>",
                    "msg": "<some text to explain the reason>"
                },
                "passed": "<overall passed/ failed"
            },
            {
                "method": "delete",
                "parameters": [
                    "person3"
                ],
                "requestId": "<id of the request>",
                "requestStatus": "<status can be true/ false; true, if request is successful>",
                "requestMsg": "<msg received after sending request>",
                "request": {
                    "id": "mosip.abis.delete",
                    "ver": "1.0",
                    "requestId": "<id of the request>",
                    "timestamp": "<timestamp>",
                    "referenceId": "r3"
                },
                "response": {
                    "id": "mosip.abis.delete",
                    "requestId": "<id of the request>",
                    "timestamp": "<timestamp>",
                    "returnValue": 1
                },
                "responseStructureValidation": {
                    "passed": "<true/ false, true if the response of ABIS is structurally correct>",
                    "msg": "<some text to explain the reason>"
                },
                "passed": "<overall passed/ failed"
            }
        ],
        "runId": "<name of the run that you enter before running>",
        "store": {
            "person1": {
                "name": "person1",
                "reference_id": "r1"
            },
            "person2": {
                "name": "person2",
                "reference_id": "r2"
            },
            "person3": {
                "name": "person3",
                "reference_id": "r3"
            }
        },
        "runResults": {
            "status": "passed",
            "reasonsForFailure": []
        }
    }
]
```