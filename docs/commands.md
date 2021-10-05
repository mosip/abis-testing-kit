## Helpful commands

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
* Create keystore:
Assuming password is password, alias is cbeff, keystore name is cbeff.p12
```text
keytool -genkey -alias cbeff \
    -keystore cbeff.p12 \
    -storetype PKCS12 \
    -keyalg RSA \
    -storepass password \
    -keysize 2048 \
    -dname "CN=Mark Smith, OU=JavaSoft, O=Sun, L=Cupertino, S=California, C=US"
```
* Export public key from keystore: `openssl pkcs12 -in cbeff.p12 -nokeys -out pub.pem -password pass:password`
```text
Remove additional data from pub.pem like:
Bag Attributes
    friendlyName: cbeff
    localKeyID: 54 69 6D 65 20 31 36 31 35 30 30 38 34 37 37 30 36 39 
subject=C = US, ST = California, L = Cupertino, O = Sun, OU = JavaSoft, CN = Mark Smith

issuer=C = US, ST = California, L = Cupertino, O = Sun, OU = JavaSoft, CN = Mark Smith

Keep only 
-----BEGIN CERTIFICATE-----
xxxxxxxx
-----END CERTIFICATE-----
```

* Export private key from keystore: `openssl pkcs12 -in cbeff.p12 -nodes -nocerts -out private.key -password pass:password`

* keytool -keystore cbeff.p12 -storetype pkcs12 -exportcert -file pub.crt -rfc -alias cbeff

## Generate RSA
openssl genrsa -out root.key 2048
openssl req -new -x509 -days 1826 -extensions v3_ca -key root.key -out root.crt -subj "/CN=A1/OU=A1/O=A1/L=BLR/ST=KAR/C=IN"
openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in root.key -out root.key.pkcs8