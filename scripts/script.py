import argparse
import logging
import subprocess


logging.basicConfig(filename="../debug.log", level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())
parser = argparse.ArgumentParser(description='Script to setup testing kit')

# General Arguments
subparsers = parser.add_subparsers(dest='mode', help='sub-command help')
subparsers.required = True
subparsers.add_parser('setup', help='Setup docker container')
subparsers.add_parser('rollback', help='Run rollback')
subparsers.add_parser('image', help='Create image')
subparsers.add_parser('rmimage', help='Remove image')
subparsers.add_parser('container', help='Create and start container')
subparsers.add_parser('rmcontainer', help='Remove container')
subparsers.add_parser('logs', help='Get logs')
args = parser.parse_args()
print(args)


def build_image():
    try:
        ds = subprocess.Popen(['docker', 'build', '-t', 'abis-testing-kit', './../'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logging.error(ds.stderr)
        while True:
            output = ds.stdout.readline()
            if output == b'' and ds.poll() is not None:
                break
            if output:
                logging.info(output.strip())
    except subprocess.CalledProcessError as e:
        logging.error(e.output)
        exit(1)


def create_container():
    try:
        ds = subprocess.Popen(['docker', 'create', '--name', 'abis-testing-kit', '-p', '8000:8000', '--log-driver', 'json-file', 'abis-testing-kit'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logging.error(ds.stderr)
        while True:
            output = ds.stdout.readline()
            if output == b'' and ds.poll() is not None:
                break
            if output:
                logging.info(output.strip())
    except subprocess.CalledProcessError as e:
        logging.error(e.output)
        exit(1)


def start_container():
    try:
        ds = subprocess.Popen(['docker', 'start', 'abis-testing-kit'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logging.error(ds.stderr)
        while True:
            output = ds.stdout.readline()
            if output == b'' and ds.poll() is not None:
                break
            if output:
                logging.info(output.strip())
    except subprocess.CalledProcessError as e:
        logging.error(e.output)
        exit(1)


def stop_container():
    try:
        ds = subprocess.Popen(['docker', 'stop', 'abis-testing-kit'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logging.error(ds.stderr)
        while True:
            output = ds.stdout.readline()
            if output == b'' and ds.poll() is not None:
                break
            if output:
                logging.info(output.strip())
    except subprocess.CalledProcessError as e:
        logging.error(e.output)
        exit(1)


def remove_container():
    try:
        ds = subprocess.Popen(['docker', 'rm', 'abis-testing-kit'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logging.error(ds.stderr)
        while True:
            output = ds.stdout.readline()
            if output == b'' and ds.poll() is not None:
                break
            if output:
                logging.info(output.strip())
    except subprocess.CalledProcessError as e:
        logging.error(e.output)
        exit(1)


def remove_image():
    try:
        ds = subprocess.Popen(['docker', 'rmi', 'abis-testing-kit'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logging.error(ds.stderr)
        while True:
            output = ds.stdout.readline()
            if output == b'' and ds.poll() is not None:
                break
            if output:
                logging.info(output.strip())
    except subprocess.CalledProcessError as e:
        logging.error(e.output)
        exit(1)


def logs():
    try:
        ds = subprocess.Popen(['docker', 'logs', 'abis-testing-kit'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logging.error(ds.stderr)
        while True:
            output = ds.stdout.readline()
            if output == b'' and ds.poll() is not None:
                break
            if output:
                logging.info(output.strip())
    except subprocess.CalledProcessError as e:
        logging.error(e.output)
        exit(1)


def setup():
    build_image()
    create_container()
    start_container()


def rollback():
    stop_container()
    remove_container()
    remove_image()


if args.mode == 'setup':
    setup()
elif args.mode == 'rollback':
    rollback()
elif args.mode == 'image':
    build_image()
elif args.mode == 'rmimage':
    remove_image()
elif args.mode == 'container':
    create_container()
    start_container()
elif args.mode == 'rmcontainer':
    stop_container()
    remove_container()
elif args.mode == 'logs':
    logs()
