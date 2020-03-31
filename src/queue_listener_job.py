import os
import time
import sys
import django

print(sys.path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()
from server.tasks import get_response_from_queue


def run_job():
    i = 1
    while True:
        print("run_job --> " + str(i))
        stat = get_response_from_queue()
        if stat is True:
            print("task completed")
        else:
            print("task not completed")
            time.sleep(10)
        i += 1


if __name__ == "__main__":
    run_job()
