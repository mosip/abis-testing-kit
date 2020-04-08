# ABIS testing kit
Provides a test framework for testing ABIS

**Requirements**
* python3 > 3.6.x; python3 --version
* docker > 19.x.x; 

**Setup**
* create a .env file in the repository root using the .evn.example file.
* update the .env with your properties.
* add your data in REPO_ROOT/sample_data including test_cases.json, test_data.json, respective cbeff files. Default files have already been added if you just want to try.
* go to REPO_ROOT/scripts folder.
* run "python3 script.py setup"; this will create a docker image and run it.
* for rollback, use "python3 script.py rollback".

**Dummy ABIS**
* go to REPO_ROOT/src
* run "python3 dummy_abis.py"; it will start a dummy abis to analyse the request and return responses in queues. 



**Contents**
* [Design diagram](./docs/images/ABIS-kit%20diagram.jpg)
* [ABIS APIs](./docs/apis.md)
* [CBEFF related info](./docs/cbeff.xml.md)