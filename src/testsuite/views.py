import json
import os
import logging
import random
import string
import traceback

from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, FileResponse, HttpResponseServerError
from django.shortcuts import render
from django.views.generic.base import View
from django.forms.models import model_to_dict

from orchestrator.encryption import Encryption
from orchestrator.orchestrator_methods import save_file, create_zip, extract_testdata, cleanTmp
from config.settings_override import app_config, queue_config
from .models import Tests, RequestMap, Logs

logger = logging.getLogger("server.custom")
abs_tmp_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../../', 'tmp'))
abs_store_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', 'store'))
abs_data_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', 'data'))
abs_result_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', 'result'))
abs_config_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', 'config'))


def index(request):
    return render(request, 'testsuite/index.html')


def settings(request):
    return render(request, 'testsuite/settings.html')


def testdata(request):
    return render(request, 'testsuite/testdata.html')


# class Generate(View):
#
#     @staticmethod
#     @swagger_auto_schema(operation_description="description")
#     def post(request, *args, **kwargs):
#         more_info = []
#         logger.info("data path: " + abs_data_path)
#         if os.path.exists(abs_data_path):
#             dir_count = 0
#             file_count = 0
#             for dir_name in os.listdir(abs_data_path):
#                 individual_folder_path = os.path.join(abs_data_path, dir_name)
#                 if os.path.isdir(individual_folder_path):
#                     dir_count = dir_count + 1
#                     biometrics = []
#                     for file_name in os.listdir(individual_folder_path):
#                         individual_file_path = os.path.join(individual_folder_path, file_name)
#                         if os.path.isfile(individual_file_path):
#                             file_count = file_count + 1
#                             bio_response, biometric, err_msg = parse_biometric_file(file_name, individual_file_path)
#                             if bio_response is True:
#                                 biometrics.append(biometric)
#                                 logger.info("folder: " + dir_name + ", file: " + file_name + ", successful")
#                             else:
#                                 logger.info(
#                                     "folder: " + dir_name + ", file: " + file_name + ", error: invalid file, info: " + err_msg)
#                                 return JsonResponse(
#                                     {"status": False, "msg": "invalid file " + file_name + ", " + err_msg})
#
#                     cbeff_file_name = dir_name + "_cbeff.xml"
#                     create_cbeff(biometrics, os.path.join(abs_store_path, cbeff_file_name))
#             logger.info("total folders: " + str(dir_count) + ", total files: " + str(file_count))
#             msg = "data generated and stored in store directory.\n" + '\n'.join(more_info)
#             return JsonResponse({"status": True, "msg": "data generated"})
#         else:
#             return JsonResponse({"status": False, "msg": "data directory not found"})


class StartRun(View):

    def post(self, request, *args, **kwargs):
        run_id = request.POST['run_name'] if request.POST['run_name'] else ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        run_type = "sync" if request.POST['run_type'] == "sync" else "async"

        """ removing previous data """
        if os.path.exists(abs_result_path):
            for item in os.listdir(abs_result_path):
                os.remove(os.path.join(abs_result_path, item))
        Tests.objects.all().delete()
        RequestMap.objects.all().delete()
        Logs.objects.all().delete()
        td = Tests(run_id=run_id, run_type=run_type, status='created')
        td.save()
        Logs(run_id=run_id, log="Run name: "+run_id+" entry has been created. Waiting for job to process it.").save()
        return JsonResponse({"status": True, "msg": model_to_dict(td)})

    def get(self, request, run_id):
        abs_file_path = os.path.join(abs_result_path, run_id+'.json')
        logger.info("get test abs file path: " + abs_file_path)
        if os.path.isfile(abs_file_path):
            try:
                with open(abs_file_path, 'r') as f:
                    file_data = f.read()
                file_data = json.loads(file_data)
                return JsonResponse(file_data, json_dumps_params={'indent': 2}, safe=False)
            except IOError:
                response = HttpResponseNotFound('<h1>File not exist</h1>')
                return response
        return HttpResponseNotFound('<h1>Test result does not exist</h1>')


class CancelRun(View):

    def post(self, request, *args, **kwargs):
        """ removing previous data """
        if os.path.exists(abs_result_path):
            for item in os.listdir(abs_result_path):
                os.remove(os.path.join(abs_result_path, item))
        Tests.objects.all().delete()
        RequestMap.objects.all().delete()
        Logs.objects.all().delete()
        return JsonResponse({"status": True, "msg": "Run successfully canceled"})


class RunStatus(View):

    def post(self, request):
        test = Tests.objects.all().first()
        if test is not None:
            logs = list(Logs.objects.filter(run_id=test.run_id).values("run_id", "log"))
        else:
            logs = []
        if test is None:
            return JsonResponse({"status": True, "msg": False})
        else:
            return JsonResponse({"status": True, "msg": model_to_dict(test), "logs": logs})


def get_cbeff(request, reference_id):
    if os.path.exists(abs_store_path):
        for filename in os.listdir(abs_store_path):
            if filename == reference_id+'.xml':
                abs_file_path = os.path.join(abs_store_path, filename)
                try:
                    with open(abs_file_path, 'r') as f:
                        file_data = f.read()

                    # encrypting data
                    if os.getenv("atk.encryption") == 'y':
                        e = Encryption()
                        data = e.encrypt_data_abis_with_0_9_specs(file_data)
                    else:
                        data = file_data
                    # sending response
                    response = HttpResponse(data)
                    return response
                except IOError:
                    response = HttpResponseNotFound('<h1>File not exist</h1>')
                    return response
    return HttpResponseNotFound('<h1>File not exist</h1>')


def get_sample_settings(request):
    abs_settings_path = os.path.join(abs_config_path, 'sample_settings.json')
    if os.path.isfile(abs_settings_path):
        with open(abs_settings_path, 'r') as f:
            file_data = f.read()
            # sending response
            response = HttpResponse(file_data, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="sample_settings.json"'
            return response
    else:
        return HttpResponseNotFound('<h1>File not exist</h1>')


def get_current_config(request):
    app_conf = app_config()._asdict()
    queue_conf = queue_config()._asdict()
    queue_conf.update(app_conf)
    return JsonResponse({"status": True, "msg": queue_conf})


class UploadOverrideSettings(View):

    def post(self, request, *args, **kwargs):
        """ removing previous data """
        file = request.FILES['file']
        if file is not None:
            settings = file.read().decode("utf-8")
            try:
                settings = json.loads(settings)
            except ValueError as e:
                print(e)
                return JsonResponse({"status": False, "msg": "Invalid json file: "+str(e)})
            path = os.path.join(abs_config_path, 'settings.json')
            save_file(path, settings)
            return JsonResponse({"status": True, "msg": "Settings uploaded successfully"}, json_dumps_params={'indent': 2})
        else:
            return JsonResponse({"status": False, "msg": "No settings file was attached"}, json_dumps_params={'indent': 2})


def get_current_testdata(View):
    try:
        zip_path = os.path.join(abs_tmp_path, 'testdata.zip')

        if os.path.isfile(zip_path):
            os.remove(zip_path)

        if not os.path.exists(abs_tmp_path):
            os.makedirs(abs_tmp_path)

        create_zip(abs_store_path, zip_path)
        zip_file = open(zip_path, 'rb')
        return FileResponse(zip_file)
    except Exception as e:
        print(e)
        print(traceback.print_tb(e.__traceback__))
        return HttpResponseServerError()


def get_sample_testdata(View):
    try:
        zip_path = os.path.join(abs_tmp_path, 'testdata.zip')

        if os.path.isfile(zip_path):
            os.remove(zip_path)

        if not os.path.exists(abs_tmp_path):
            os.makedirs(abs_tmp_path)

        create_zip(abs_store_path, zip_path)
        zip_file = open(zip_path, 'rb')
        return FileResponse(zip_file)
    except Exception as e:
        print(e)
        print(traceback.print_tb(e.__traceback__))
        return HttpResponseServerError()


class UploadTestData(View):

    def post(self, request, *args, **kwargs):
        """ removing previous data """
        cleanTmp()
        try:
            fs = request.FILES['file']
            if fs is not None:
                file = open(os.path.join(abs_tmp_path, 'testdata.zip'), 'wb')
                file.write(fs.read())
                file.close()
                extract_testdata(os.path.join(abs_tmp_path, 'testdata.zip'))
                return JsonResponse({"status": True, "msg": "Settings uploaded successfully"})
            else:
                return JsonResponse({"status": False, "msg": "No settings file was attached"})
        except Exception as e:
            print(e)
            print(traceback.print_tb(e.__traceback__))
            return JsonResponse({"status": False, "msg": str(e)})
