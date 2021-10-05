import logging
import os
import pprint

rootPath = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), './')
)

logPath = os.path.abspath(
    os.path.join(rootPath, 'logs', 'out.log')
)


def initLogger(log_file=None):
    if log_file is None:
        log_file = logPath
    logging.basicConfig(filename=log_file, filemode='w', level=logging.INFO)
    root_logger = logging.getLogger()
    console_handler = logging.StreamHandler()
    root_logger.addHandler(console_handler)


def myPrint(msg, head=None):
    if msg is None:
        return
    if head == 1:
        logging.info('\n\n=================================================================== ')
        logging.info(Colors.HEADER + Colors.BOLD + (pprint.pformat(msg) if not isStr(msg) else msg) + Colors.ENDC)
    elif head == 2:
        logging.info('\n')
        logging.info(Colors.OKBLUE + ((pprint.pformat(msg) if not isStr(msg) else msg) + Colors.ENDC))
    elif head == 3:
        logging.info(Colors.OKBLUE + "- " + ((pprint.pformat(msg) if not isStr(msg) else msg) + Colors.ENDC))
    elif head == 4:
        logging.info("- " + (pprint.pformat(msg) if not isStr(msg) else msg))
    elif head == 11:
        logging.info(Colors.WARNING + "- " + (pprint.pformat(msg) if not isStr(msg) else msg) + Colors.ENDC)
    elif head == 12:
        logging.info(Colors.OKGREEN + "- " + (pprint.pformat(msg) if not isStr(msg) else msg) + Colors.ENDC)
    elif head == 13:
        logging.info(Colors.FAIL + (pprint.pformat(msg) if not isStr(msg) else msg) + Colors.ENDC)
    else:
        logging.info("- " + (pprint.pformat(msg) if not isStr(msg) else msg))


def isStr(s):
    return isinstance(s, str)


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