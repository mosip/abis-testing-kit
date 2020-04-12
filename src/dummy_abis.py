import os
import time
import sys
import django
import random
print(sys.path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from config.settings import QueueConfig
from config.settings_override import queue_config
from orchestrator.queue_methods import consume, produce


def run_job():
    i = 1
    while True:
        try:
            conf = queue_config()
            status, body = consume(conf.host, conf.send_address, conf.user, conf.password, 'dummy_abis')
            if status is True:
                print("Message found")
                print(str(body))
                res_id = body['id']
                request_id = body['requestId']
                ret_val = random.randint(1, 2)
                if ret_val == 1:
                    response = {
                        "id": body['id'],
                        "requestId": body['requestId'],
                        "timestamp": str(int(time.time())),
                        "returnValue": ret_val
                    }
                else:
                    response = {
                        "id": body['id'],
                        "requestId": body['requestId'],
                        "timestamp": str(int(time.time())),
                        "returnValue": ret_val,
                        "failureReason": random.randint(3, 9),
                    }
                r_status, r_body = produce(response, conf.host, conf.consume_address, conf.user, conf.password)
                if r_status is True:
                    print(r_body)
                    print("Message delivered")
                else:
                    print("Message not delivered")
            else:
                print("No message found")
            time.sleep(2)
        except Exception as e:
            print("OS error: {0}".format(e))
            time.sleep(10)


if __name__ == "__main__":
    run_job()
