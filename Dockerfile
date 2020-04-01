FROM ubuntu:18.04

COPY . /opt/abis-testing-kit/
COPY sample_data/ /opt/abis-testing-kit/src/store/

RUN apt-get update \
    && apt-get -y install curl wget git bash python3 python3-pip default-jdk \
    && cd /opt \
    && wget http://apachemirror.wuchna.com//activemq/5.15.12/apache-activemq-5.15.12-bin.tar.gz \
    && tar zxf apache-activemq-5.15.12-bin.tar.gz \
    && ln -s /opt/apache-activemq-5.15.12 activemq \
#    && git clone https://github.com/mosip/abis-testing-kit.git \
    && cd /opt/abis-testing-kit \
    && pip3 install -r requirements.txt \
    && cd src \
    && python3 manage.py migrate \
    && chmod +x /opt/abis-testing-kit/run.sh

EXPOSE 8000

#CMD ["tail", "-f", "/dev/null"]
ENTRYPOINT ["/opt/abis-testing-kit/run.sh"]
CMD ["run"]
