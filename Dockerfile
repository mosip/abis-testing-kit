FROM ubuntu:18.04

COPY . /opt/abis-testing-kit/
COPY sample_data/ /opt/abis-testing-kit/src/store/

RUN apt-get update \
    && apt-get -y install curl wget git bash python3 python3-pip \
    && cd /opt/abis-testing-kit \
    && pip3 install -r requirements.txt \
    && cd src \
    && python3 manage.py migrate \
    && chmod +x /opt/abis-testing-kit/scripts/run.sh

EXPOSE 8000
EXPOSE 8161
#CMD ["tail", "-f", "/dev/null"]
ENTRYPOINT ["/opt/abis-testing-kit/scripts/run.sh"]
CMD ["run"]
