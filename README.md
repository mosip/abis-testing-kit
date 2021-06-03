# ABIS testing kit
Provides a test framework for testing ABIS

## Requirements
* python3 > 3.6.x; python3 --version
* docker > 19.x.x; docker -v

## Setup

### Direct setup
* add public key (.pem) to REPO_ROOT/src/config/certificates folder
* create a .env file in the repository root using the .env.example file.
* update the .env with your properties.
* add your data in REPO_ROOT/sample_data including test_cases.json, test_data.json, respective cbeff files. Default files have already been added if you just want to try.
* Copy files inside REPO_ROOT/sample_data to REPO_ROOT/src/store
* Go to REPO_ROOT and run `pip3 install -r requirements.txt`
* Go to REPO_ROOT/src and run `python3 manage.py migrate`
* Go to REPO_ROOT/src and run `python3 manage.py runserver`
* open `localhost:8000` to view the UI

### Via docker
* add public key (.pem) to REPO_ROOT/src/config/certificates folder
* create a .env file in the repository root using the .env.example file.
* update the .env with your properties.
* add your data in REPO_ROOT/sample_data including test_cases.json, test_data.json, respective cbeff files. Default files have already been added if you just want to try.
* go to REPO_ROOT/scripts folder.
* run "python3 script.py setup"; this will create a docker image and run it.
* open `localhost:8000` to view the UI
* for rollback, use "python3 script.py rollback".

### Generate RSA certificate
Go to src/config/certificates folder

Run below commands in sequence:
* openssl genrsa -out root.key 2048
* openssl req -new -x509 -days 1826 -extensions v3_ca -key root.key -out root.crt -subj "/CN=A1/OU=A1/O=A1/L=BLR/ST=KAR/C=IN"
* openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in root.key -out root.key.pkcs8

Above commands will create a root.crt, root.key, root.key.pkcs8 files in certificates folder
* root.crt will be used for encryption
* root.key or root.key.pkcs8 can be used for decryption

### Dummy ABIS (Optional, just for testing the test-kit)
* Go to REPO_ROOT/src
* run "python3 dummy_abis.py"; it will start a dummy abis to analyse the request and return responses in queues. 

### Activemq setup for local testing
* Go to REPO_ROOT/support/activemq
* Run docker-compose file, it will create a docker container that can be used for local testing

## Common list test cases
* [list of test cases](./docs/testcases.md)

## Documentation
* [How to write test cases](./docs/testcase.json.md)
* [How to add test data](./docs/personadata.md)
* [Sample test and result analysis](./docs/sample.md)


## Contents
* [Design diagram](./docs/images/ABIS-kit%20diagram.jpg)
* [ABIS APIs](./docs/apis.md)
* [CBEFF related info](./docs/cbeff.xml.md)