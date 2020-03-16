import os
import logging
import uuid

from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.generic.base import View
from drf_yasg.utils import swagger_auto_schema

from .utils import produce, consume, parse_biometric_file
from src.abis_apis.lib import insert as insert_request
from src.cbeff import create as create_cbeff
from testsuite.models import TestCase
from src.config.settings import AppConfig

logger = logging.getLogger("server.custom")


def index(request):
    return HttpResponse('App is running.')


class Generate(View):

    @staticmethod
    @swagger_auto_schema(operation_description="description")
    def post(request, *args, **kwargs):
        more_info = []
        abs_store_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', 'store'))
        data_path = "data"
        abs_data_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', data_path))
        logger.info("data path: " + abs_data_path)
        if os.path.exists(abs_data_path):
            dir_count = 0
            file_count = 0
            for dir_name in os.listdir(abs_data_path):
                individual_folder_path = os.path.join(abs_data_path, dir_name)
                if os.path.isdir(individual_folder_path):
                    dir_count = dir_count + 1
                    biometrics = []
                    for file_name in os.listdir(individual_folder_path):
                        individual_file_path = os.path.join(individual_folder_path, file_name)
                        if os.path.isfile(individual_file_path):
                            file_count = file_count + 1
                            bio_response, biometric, err_msg = parse_biometric_file(file_name, individual_file_path)
                            if bio_response is True:
                                biometrics.append(biometric)
                                logger.info("folder: " + dir_name + ", file: " + file_name + ", successful")
                            else:
                                logger.info(
                                    "folder: " + dir_name + ", file: " + file_name + ", error: invalid file, info: " + err_msg)
                                return JsonResponse(
                                    {"status": False, "msg": "invalid file " + file_name + ", " + err_msg})

                    cbeff_file_name = dir_name + "_cbeff.xml"
                    create_cbeff(biometrics, os.path.join(abs_store_path, cbeff_file_name))
            logger.info("total folders: " + str(dir_count) + ", total files: " + str(file_count))
            msg = "data generated and stored in store directory.\n" + '\n'.join(more_info)
            return JsonResponse({"status": True, "msg": "data generated"})
        else:
            return JsonResponse({"status": False, "msg": "data directory not found"})


class Clear(View):
    @swagger_auto_schema(operation_description="description")
    def post(self, request, *args, **kwargs):
        abs_store_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', 'store'))
        if os.path.exists(abs_store_path):
            for item in os.listdir(abs_store_path):
                if item.endswith(".xml"):
                    os.remove(os.path.join(abs_store_path, item))
        return JsonResponse({"status": True, "msg": "All generated cbeff files have been removed"})


class RunTest(View):

    def post(self, request, *args, **kwargs):
        tests_count = 0
        """ Removing previous data """
        TestCase.objects.all().delete()

        """ Fetching the data """
        abs_store_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', 'store'))
        if os.path.exists(abs_store_path):
            for filename in os.listdir(abs_store_path):
                if filename.endswith(".xml"):
                    request_id = uuid.uuid1().hex
                    reference_id = str(filename.split('_')[0])
                    test_case_id = uuid.uuid1().hex
                    request = insert_request(request_id, reference_id, AppConfig.callback_url)
                    """ Saving to database """
                    tc = TestCase(request_id=request_id, reference_id=reference_id, test_case_id=test_case_id)
                    tc.save()
                    logger.info(
                        "request_id=" + request_id + ", reference_id=" + reference_id + ", test_case_id=" + test_case_id + " saved to db")
                    """ Sending to queue """
                    status, body = produce(request)
                    if status:
                        tests_count = tests_count + 1
                        logger.info(body)
                        logger.info(
                            "request_id=" + request_id + ", reference_id=" + reference_id + ", test_case_id=" + test_case_id + " sent to queue")
                    else:
                        logger.info(body)
                        return JsonResponse(
                            {"status": False, "msg": "Unable to add to queue"})
        return JsonResponse({"status": True, "msg": str(tests_count) + " tests successfully initiated."})


class InsertEntry(View):

    def post(self, request, *args, **kwargs):
        data = insert_request("32323", "dsdsdsf", "dsdsdsfsfsfsfsf")
        d = produce(data)
        return HttpResponse(d)


class GetEntry(View):

    def get(self, request, *args, **kwargs):
        status, body = consume()
        if status:
            logger.info(body)
        else:
            logger.info(body)
            return JsonResponse({"status": False, "msg": body})
        return JsonResponse({"status": True, "msg": body})


class GetCbeff(View):

    def get(self, request, reference_id):
        abs_store_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', 'store'))
        if os.path.exists(abs_store_path):
            for filename in os.listdir(abs_store_path):
                if filename.endswith(".xml") and filename.split('_')[0] == reference_id:
                    abs_file_path = os.path.join(abs_store_path, filename)
                    try:
                        with open(abs_file_path, 'r') as f:
                            file_data = f.read()

                        # sending response
                        response = HttpResponse(file_data, content_type='application/xml')
                        response['Content-Disposition'] = 'attachment; filename="cbeff.xml"'
                        return response
                    except IOError:
                        response = HttpResponseNotFound('<h1>File not exist</h1>')
                        return response
        return HttpResponseNotFound('<h1>File not exist</h1>')
