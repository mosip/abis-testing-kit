# settings.py
import json
import os
from collections import namedtuple
from typing import Dict, Type

from dotenv import load_dotenv
from pathlib import Path  # python3 only
load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)


class QueueConfig:
    """ Queue related config """
    host = os.getenv("atk.queue.host")  # default 'http://localhost'
    port = os.getenv("atk.queue.port")  # default '8161'
    user = os.getenv("atk.queue.user")  # default 'admin'
    password = os.getenv("atk.queue.password")  # 'admin'
    send_address = os.getenv("atk.queue.send_address")  # 'm2a'
    consume_address = os.getenv("atk.queue.consume_address")  # 'a2m'
    client_id = os.getenv("atk.queue.client_id")  # 'any string'


class AppConfig:
    """ App config """
    callback_url = os.getenv("atk.app.callback_url")  # default 'http://localhost:8000/'
    abis_response_timeout = os.getenv("atk.app.abis_response_timeout")
    abis_threshold = os.getenv("atk.app.abis_threshold")

