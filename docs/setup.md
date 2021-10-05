## Setup docs for Ubuntu

**Requirements**
* Ubuntu >= 16.04
* Python version >= 3.6.9


### How to setup
* Create a virtual environment > python3 -m venv venv
* Activate virtual env > source venv/bin/activate
* download dependencies > pip install -r requirements.txt
* Go to server folder where manage.py is located, run python manage.py runserver to start development server

### Active MQ
* docker pull rmohr/activemq
* docker run -p 61616:61616 -p 8161:8161 rmohr/activemq