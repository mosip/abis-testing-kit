import os
import time
import sys
import django

from testsuite.utils import init_logger

print(sys.path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()
from server.tasks import run_orchestrator

abs_log_path = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'logs')
)

init_logger(os.path.join(abs_log_path, 'debug.log'))


def run_job():
    i = 1
    while True:
        print("run_job --> " + str(i))
        stat = run_orchestrator()
        if stat is True:
            print("task completed")
            time.sleep(10)
        else:
            print("task not completed")
            time.sleep(10)
        i += 1


if __name__ == "__main__":
    run_job()
