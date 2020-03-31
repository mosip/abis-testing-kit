import os
import time
import sys
import django
import random
from config.settings import Queue
from orchestrator import consume, produce

print(sys.path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()


def run_job():
    i = 1
    while True:
        try:
            status, body = consume(Queue.send_address, 'dummy_abis')
            if status is True:
                print("Message found")
                res_id = body['id']
                request_id = body['requestId']
                response = {
                    "id": body['id'],
                    "requestId": body['requestId'],
                    "timestamp": str(int(time.time())),
                    "returnValue": random.randint(1, 2)
                }
                r_status, r_body = produce(Queue.consume_address, response)
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
