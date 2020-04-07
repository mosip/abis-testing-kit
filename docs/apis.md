# Insert

Insert biometric data of an Individual. [reference](https://github.com/mosip/documentation/wiki/ABIS-APIs)

* ABIS must get biometric data from referenceURL, process it and store it locally within the ABIS reference database
* referenceId must not be active prior to this operation i.e., it must not have been used before this operation
* De-duplication must not be performed in this operation
* MOSIP must provide CBEFF format biometric data to ABIS


### Request

``` json
{
    "id" : "mosip.abis.insert",
    "ver" : "1.0",
    "requestId" : "01234567-89AB-CDEF-0123-456789ABCDEF",
    "timestamp" : "1539777717",
    "referenceId" : "01234567-89AB-CDEF-0123-456789ABCDEF",
    "referenceURL" : "https://mosip.io/biometric/45678"
            
}
```


_where_
* requestId is an uuid for every request
* referenceId is an uuid associated with a single record
* referenceURL is a callback url, using which ABIS will get the biometric data



### Response

``` json
{
    "id" : "mosip.abis.insert",
    "requestId" : "01234567-89AB-CDEF-0123-456789ABCDEF",
    "timestamp" : "1539777717",
    "returnValue" : 1
}
```
_where_
* returnValue: 1 means success, not 1 means failure




# Identity

Identify biometric data of an Individual. [reference](https://github.com/mosip/documentation/wiki/ABIS-APIs)

* IDENTIFY request MUST provide a 1:n comparison
* The input set for comparison can be provided by referenceID
* The collection against which the input set has to be matched is specified by a set of referenceID's. If referenceId is provided, atleast one referenceID must be provided in the input. The provided referenceID's must be present in the reference database.
* If IDENTIFY is against all the entries in ABIS, then gallery attribute MUST not be specified
* maxResults specify how many results can be returned. By default this will be 10
* IDENTIFY should give all candidates which match targetFIPR or a better score than the targetFIPR
* This request should not match against referenceID that is not in the reference database
* If referenceID is not NULL, then, ABIS performs 1:n comparison against all the entries in ABIS using the referenceID
* If referenceID is NULL and referenceURL is provided, then, ABIS performs 1:n comparison against all the entries in ABIS using the referenceURL
* If referenceID and reference URL both are NULL, then, ABIS throws an error (error code 5)


### Request

``` json
{
    "id" : "mosip.abis.identify",
    "ver" : "1.0",
    "requestId" : "01234567-89AB-CDEF-0123-456789ABCDEF",
    "timestamp" : "1539777717",
    "referenceId" : "987654321-89AB-CDEF-0123-456789ABCDEF",
    "referenceUrl" : "https://mosip.io/registrationprocessor/v1/bio-dedupe/biometricfile/2cce7b7d-b58a-4466-a006-c79297281789",
    "maxResults" : 10,
    "targetFPIR" : 30,
    "gallery" : {
        "referenceIds" : [
            {
                "referenceId" : "2cce7b7d-b58a-4466-a006-c79297281123"
            }, 
            {
                "referenceId" : "2cce7b7d-b58a-4466-a006-c79297281456"
            }, 
            {
                "referenceId" : "2cce7b7d-b58a-4466-a006-c79297281678"
            }, 
            {
                "referenceId" : "2cce7b7d-b58a-4466-a006-c79297281098"
            }, 
            {
                "referenceId" : "2cce7b7d-b58a-4466-a006-c79297281321"
            } 
        ]
    }
}
```


_where_
* requestId is an uuid for every request
* referenceId is an uuid associated with a single record
* referenceURL is a callback url, using which ABIS will get the biometric data



### Response

``` json
{
    "id" : "mosip.abis.identify",
    "requestId" : "01234567-89AB-CDEF-0123-456789ABCDEF",
    "timestamp" : "1539777717",
    "returnValue" : 1,
    "candidateList" : {
        "count" : "2",
        "candidates" : [    
            {
                "referenceId" : "x",
                "internalScore": "<abis specific>",
                "scaledScore" : "<abis specific> 0-100",
                "analytics": [
                    {
                        "key1": "value1",
                        "key2": "value2"
                    }
                ],
                "scores": [
                    {
                        "biometricType": "FIR",
                        "scaledScore": "",
                        "internalScore": "",
                        "analytics": [
                            {
                                "key1": "value1",
                                "key2": "value2"
                            }
                        ]
                    },
                    {
                        "biometricType": "IIR",
                        "scaledScore": "",
                        "internalScore": "",
                        "analytics": [
                            {
                                "key1": "value1",
                                "key2": "value2"
                            }
                        ]
                    }
                ]
            }
        ]
    }
}
```
_where_
* returnValue: 1 means success, not 1 means failure




# Delete

* Removes only the entry referred by the referenceId
* This operation can be used to remove duplicates found by Identify

### Request

``` json
{
    "id" : "mosip.abis.delete",
    "ver" : "1.0",
    "requestId" : "01234567-89AB-CDEF-0123-456789ABCDEF",
    "timestamp" : "1539777717",
    "referenceId" : ""
}
```


_where_
* requestId is an uuid for every request
* referenceId is an uuid associated with a single record
* referenceURL is a callback url, using which ABIS will get the biometric data



### Response

``` json
{
    "id" : "mosip.abis.delete",
    "requestId" : "01234567-89AB-CDEF-0123-456789ABCDEF",
    "timestamp" : "1539777717",
    "returnValue" : 1
}
```
_where_
* returnValue: 1 means success, not 1 means failure




# Ping

* ABIS responds with the count of requests that are still pending

### Request

``` json
{
    "id" : "mosip.abis.pendingJobs",
    "ver" : "1.0",
    "requestId" : "01234567-89AB-CDEF-0123-456789ABCDEF",
    "timestamp" : "1539777717"
}
```


_where_
* requestId is an uuid for every request
* referenceId is an uuid associated with a single record
* referenceURL is a callback url, using which ABIS will get the biometric data



### Response

``` json
{
    "id" : "mosip.abis.pendingJobs",
    "requestId" : "01234567-89AB-CDEF-0123-456789ABCDEF",
    "timestamp" : "1539777717",
    "jobscount" : "",
    "returnValue" : 1
}
```
_where_
* returnValue: 1 means success, not 1 means failure




# reference count

* ABIS will send a count of records in the reference database

### Request

``` json
{
    "id" : "mosip.abis.referenceCount",
    "ver" : "1.0",
    "requestId" : "01234567-89AB-CDEF-0123-456789ABCDEF",
    "timestamp" : "1539777717"
}
```


_where_
* requestId is an uuid for every request
* referenceId is an uuid associated with a single record
* referenceURL is a callback url, using which ABIS will get the biometric data



### Response

``` json
{
    "id" : "mosip.abis.referenceCount",
    "requestId" : "01234567-89AB-CDEF-0123-456789ABCDEF",
    "timestamp" : "1539777717",
    "count" : "",
    "returnValue" : 1
}
```
_where_
* returnValue: 1 means success, not 1 means failure