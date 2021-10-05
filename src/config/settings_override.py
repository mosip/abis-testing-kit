import json
import os
from collections import namedtuple
from typing import Dict, NamedTuple

from config.settings import QueueConfig, AppConfig

abs_settings_path = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), './settings.json'))
print(abs_settings_path)
queue = namedtuple('Queue', 'host, user, password, send_address, consume_address, client_id')
app = namedtuple('App', 'callback_url, abis_response_timeout, abis_threshold')


def queue_config() -> queue:
    properties: Dict = {}
    if os.path.exists(abs_settings_path) and os.path.isfile(abs_settings_path):
        with open(abs_settings_path, 'r') as file:
            properties: Dict = json.loads(file.read())
    q = queue(
        properties["atk.queue.host"] if "atk.queue.host" in properties else QueueConfig.host,
        properties["atk.queue.user"] if "atk.queue.user" in properties else QueueConfig.user,
        properties["atk.queue.password"] if "atk.queue.password" in properties else QueueConfig.password,
        properties["atk.queue.send_address"] if "atk.queue.send_address" in properties else QueueConfig.send_address,
        properties["atk.queue.consume_address"] if "atk.queue.consume_address" in properties else QueueConfig.consume_address,
        properties["atk.queue.client_id"] if "atk.queue.client_id" in properties else QueueConfig.client_id
    )
    return q


def app_config() -> app:
    properties: Dict = {}
    if os.path.exists(abs_settings_path) and os.path.isfile(abs_settings_path):
        with open(abs_settings_path, 'r') as file:
            properties: Dict = json.loads(file.read())
    a = app(
        properties["atk.app.callback_url"] if "atk.app.callback_url" in properties else AppConfig.callback_url,
        properties["atk.app.abis_response_timeout"] if "atk.app.abis_response_timeout" in properties else AppConfig.abis_response_timeout,
        properties["atk.app.abis_threshold"] if "atk.app.abis_threshold" in properties else AppConfig.abis_threshold
    )
    return a
