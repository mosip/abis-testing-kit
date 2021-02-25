import base64
import logging
import pprint

from cbeff.biometrics import Biometrics


def parse_biometric_file(name: str, path: str):
    strs = name.split('.')[0].split('_')
    if not name.endswith('.jpeg'):
        return False, None, "only jpeg format is allowed"
    if len(strs) != 2:
        return False, None, "filename should be <Biometric type>_<Biometric subtype>"

    with open(path, 'rb') as file:
        data = file.read()
        data = base64.b64encode(data).decode('utf-8')
        print("-----------------------------------------------------------------------------------------")
        print(type(data))
    biometric = Biometrics(strs[0], strs[1], data)
    return True, biometric, None


def myprint(msg, head=None):
    if head == 1:
        logging.info('===================================================================')
        logging.info(Colors.HEADER + pprint.pformat(msg) + Colors.ENDC)
        logging.info('-------------------------------------------------------------------')
    elif head == 2:
        logging.info('=============')
        logging.info(Colors.OKBLUE + pprint.pformat(msg) + Colors.ENDC)
        logging.info('-------------')
    elif head == 3:
        logging.info(pprint.pformat(msg))
    elif head == 11:
        logging.info(Colors.WARNING + pprint.pformat(msg) + Colors.ENDC)
    elif head == 12:
        logging.info(Colors.OKGREEN + pprint.pformat(msg) + Colors.ENDC)
    elif head == 13:
        logging.info(Colors.FAIL + pprint.pformat(msg) + Colors.ENDC)
    else:
        logging.info(pprint.pformat(msg))


def init_logger(log_file):
    logging.basicConfig(filename=log_file, filemode='w', level=logging.INFO)
    root_logger = logging.getLogger()
    console_handler = logging.StreamHandler()
    root_logger.addHandler(console_handler)


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
