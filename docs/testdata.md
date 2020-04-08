## Test data

Test data json contains an array of persona data, used in test case execution

* name is the name of the the persona, name will be used in the test case to map a user
* reference_id is an unique identifier for persona, will be used to map the persona and its cbeff.xml file
* the nomenclature of the cbeff file associated to a persona is "<reference_id>.xml", and it should be placed in the same directory as the test data file

### Example

```json
[
    {
      "name": "x1",
      "reference_id":  "y1"
    },
    {
      "name": "x2",
      "reference_id":  "y2"
    }
]
```
