"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import threading
import time

from django.urls import path, include
# from testsuite.tasks import get_response_from_queue, run_orchestrator

urlpatterns = [
    path('', include('testsuite.urls'))
]

# def run_job():
#     i = 1
#     while True:
#         print("run_job --> "+str(i))
#         stat = get_response_from_queue()
#         if stat is True:
#             print("task completed")
#         else:
#             print("task not completed")
#             time.sleep(10)
#         i += 1
#
#
# job_thread = threading.Thread(target=run_job)
# job_thread.start()
#
#
# def run_orchestrator_job():
#     i = 1
#     while True:
#         print("run_job --> "+str(i))
#         stat = run_orchestrator()
#         if stat is True:
#             print("task completed")
#         else:
#             print("task not completed")
#             time.sleep(10)
#         i += 1
#
#
# job_thread2 = threading.Thread(target=run_job)
# job_thread2.start()

