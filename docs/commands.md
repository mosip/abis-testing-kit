## Helpul commands

**Commands**
* To create a virtual environment: python3 -m venv venv
* To install a new package: pip install <package_namr>
* To freeze requirements: pip freeze > requirements.txt
* Building docker images: sudo docker build -t abis-testing-kit . 
* Running docker: sudo docker run -d -it --hostname=localhost --name abis-testing-app -p 8000:8000 --log-driver json-file abis-testing-kit
* Go inside container: sudo docker exec -it abis-testing-app bash
* remove all containers: sudo docker rm -f $(sudo docker ps -a -q)
* run django inside container: python3 manage.py runserver 0.0.0.0:8000 --noreload

### Create certificate
* Go to config/certificates folder
* Generate certificates: `openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt`
* Get public key from certificate: `openssl x509 -in server.crt -pubkey -noout -outform pem`
