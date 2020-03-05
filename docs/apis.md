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

# delete

# ping

# reference count