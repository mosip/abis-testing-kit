import traceback
from config.settings_override import queue_config
from testsuite.models import RequestMap, Tests, Logs
from orchestrator.orchestration import Orchestrator
from orchestrator.queue_methods import consume
from testsuite.utils import myprint


def get_response_from_queue():
    try:
        conf = queue_config()
        print("get_response_from_queue host[" + conf.host + "] : started")
        status, body = consume(conf.host, conf.consume_address, conf.user, conf.password, conf.client_id)
        if status is True:
            request_id = body['requestId']
            request_map = RequestMap.objects.filter(request_id=request_id).first()
            if request_map is None:
                new_record = RequestMap(request_id=request_id, response=body)
                new_record.save()
            print("status: " + str(status))
            print("body: " + str(body))
            print("get_response_from_queue: ended")
            return True
        else:
            return None
    except Exception as e:
        formatted_lines = traceback.format_exc()
        myprint(formatted_lines, 13)
        print("OS error: {0}".format(e))
        return False


def run_orchestrator():
    print("get_response_from_queue: started")
    run_id = None
    try:
        test = Tests.objects.all().first()
        if test is not None and test.status not in ['completed', 'error']:
            run_id = test.run_id
            Orchestrator(test.run_id, test.run_type).run()
            Tests.objects.filter(run_id=test.run_id).update(status='completed')
            Logs(run_id=run_id, log="Run completed").save()
            return True
        else:
            return None
    except Exception as e:
        formatted_lines = traceback.format_exc()
        myprint(formatted_lines, 13)
        Tests.objects.filter(run_id=run_id).update(status='error', msg='e')
        Logs(run_id=run_id, log="Error occured: "+str(e)).save()
        return False
