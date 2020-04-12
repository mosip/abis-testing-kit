## Common list test cases

#### 1) Send insert request to abis and verify the record is inserted correctly.

* ABIS must get biometric CBEFF file from referenceURL, process it and store it locally within the ABIS reference database
* Verify the request id is same in abis response for the insert request.
* Verify the return value is 1

#### 2) Send insert request to abis with wrong reference id for which there is no biometric file present and verify abis is returning error code.

* Verify the return value is 2
* Verify the request id is same in abis response for the insert request.
* Verify failure reason is 7

#### 3) Send insert request to abis with null reference id. Abis should not be able to process the request.

* Verify the return value is 2
* Verify the request id is same in abis response for the insert request.
* Verify failure reason is 7

#### 4) Send unique identify request with maxResults, targetFPIR set in configuration. Set gallery match as null and abis should be able to identify the record against all other records present inside db.

* Verify request id is same in response as present in request.
* Verify return value is 1
* Verify candidate list has no candidates with count as 0

#### 5) Send identify request for a biometric which is duplicate against another record. Set gallery match as null and abis should be able to identify the record against all other records present inside db.

* Verify return value is 1
* Verify candidate list has one candidate with count as 1. Verify the candidate referenceId is the expected referenceId.
* Verify the scaled score is greater then configured threshold in configuration.

#### 6) Send identify request for a biometric which is duplicate against another 2 records. Set gallery match as the first duplicate candidate id and abis should be able to identify the record only against the candidate present in gallery.

* Verify return value is 1
* Verify candidate list has one candidate with count as 1. Verify the candidate referenceId is expected referenceId (the first duplicate candidate id and not the second one).
* Verify the scaled score is greater then configured threshold in configuration.

#### 7) Send identify request for a biometric which is duplicate against another 2 records. Set maxResults as 1.

* Verify ABIS has returned only one record as duplicate in descending order(the highest scaled score match).
* Verify candidate list has one candidate with count as 1. Verify the candidate referenceId is expected referenceId (the first duplicate candidate id and not the second one).
* Verify the scaled score is greater then configured threshold in configuration.

#### 8) Send identify request with reference id and reference url both as null.

* Verify abis should send returnValue as 2.
* Verify failure reason 5

#### 9) Send identify request with reference id as null and correct reference url.

* Verify abis should be able to perform dedupe by getting the cbeff from reference URL.
* Verify abis should send returnValue as 1.

#### 10) Send identify request with correct reference id and wrong reference url. Make sure if reference id is already present inside abis, it will not call reference url to get the cbeff file. Instead it will compare against the cbeff file stored inside abis.

#### 11) Send delete request with correct request id and reference id.

* ABIS should be able to delete the record successfully.
* Try to send identify request for the reference id and it should fail in ABIS since the record was deleted earlier.

#### 12) Send delete request with wrong reference id.

* ABIS should send return value as 2 with failure reason.

#### 13) Send ping request with request id.

* ABIS should respond with return value 1.