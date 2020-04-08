## Test cases

A test case json file contains an array of test object that contains the necessary to run tests

* testId can be a unique identifier for a test
* testDescription, description of the test
* steps, a list of function to execute with the persona name in "()"

### Steps

**insert(persona)**

* sends an insert request to the queue with the reference id of the persona. 
* callback url will be sent in request from which the ABIS will fetch cbeff associated with the persona

[know more about request](./../docs/apis.md#Insert)

**identify(persona_1, persona_2, persona_3,..,...)**

* sends an identify request to the queue with the reference id of person_1
* gallery of reference ids of persona_2, persona_3,...
* if only persona_1 is provided, then it will send no gallery and the match will happen with all inserted data

[know more about request](./../docs/apis.md#Identify)

**identify_url(persona_1, persona_2, persona_3,..,...)**

* sends an identify request to the queue with the reference url of person_1
* gallery of reference ids of persona_2, persona_3,...
* if only persona_1 is provided, then it will send no gallery and the match will happen with all inserted data

[know more about request](./../docs/apis.md#Identify)

**delete(persona_1)**

* sends an delete request to the queue with the reference id of person_1

[know more about request](./../docs/apis.md#Delete)

**ping**

* sends an ping request to the queue to get pending Jobs count

[know more about request](./../docs/apis.md#Ping)

**reference_count**

* sends an reference_count request to the queue

[know more about request](./../docs/apis.md#Reference count)

### Example

```json
[
    {
        "testId": "x1",
        "testDescription": "y1",
        "steps": [
            "insert(person1)", "insert(person2)", "identify(person3, person1, person2)"
        ]
    },
    {
        "testId": "x2",
        "testDescription": "y2",
        "steps": [
            "insert(person1)", "insert(person2)", "identify(person3, person1, person2)"
        ]
    }
]
```