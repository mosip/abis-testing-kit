# ABIS testing kit
Provides a test framework for testing ABIS

**Commands**

* To install a new package: pip install <package_namr>
* To freeze requirements: pip freeze > requirements.txt
* Building docker images: sudo docker build -t abis-testing-kit . 
* Running docker: sudo docker run -d -it --hostname=localhost --name abis-testing-app -p 8000:8000 --log-driver json-file abis-testing-kit
* Go inside container: sudo docker exec -it abis-testing-app bash
* remove all containers: sudo docker rm -f $(sudo docker ps -a -q)

**Contents**
* [Design diagram](./docs/images/ABIS-kit%20diagram.jpg)
* [ABIS APIs](./docs/apis.md)
* [CBEFF related info](./docs/cbeff.xml.md)