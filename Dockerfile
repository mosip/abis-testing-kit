FROM ubuntu:18.04

RUN apt-get update && apt-get -y install curl git python3 python3-pip \
    && cd /opt \
    && git clone https://github.com/mosip/abis-testing-kit.git \
    && cd /opt/abis-testing-kit \
    && pip3 install -r requirements.txt

