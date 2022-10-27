import logging
import time
from argparse import ArgumentParser
from flask import Flask
from functools import wraps
from gqlalchemy import Memgraph


log = logging.getLogger(__name__)


def init_log():
    logging.basicConfig(level=logging.DEBUG)
    log.info("Logging enabled")
    logging.getLogger("werkzeug").setLevel(logging.WARNING)


init_log()


def parse_args():
    '''
    Parse command line arguments.
    '''
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--app-host", default="0.0.0.0",
                        help="Allowed host addresses.")
    parser.add_argument("--app-port", default=5000, type=int,
                        help="App port.")
    parser.add_argument("--template-folder", default="public/template",
                        help="The folder with flask templates.")
    parser.add_argument("--static-folder", default="public",
                        help="The folder with flask static files.")
    parser.add_argument("--debug", default=True, action="store_true",
                        help="Run web server in debug mode")
    print(__doc__)
    return parser.parse_args()


args = parse_args()


def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        log.info(f"Time for {func.__name__} is {duration}")
        return result
    return wrapper


app = Flask(__name__)


memgraph = Memgraph()
connection_established = False
while(not connection_established):
    try:
        if (memgraph._get_cached_connection().is_active()):
            connection_established = True
    except:
        log.info("Memgraph probably isn't running.")
        time.sleep(4)


@log_time
def generate_data():
    memgraph.drop_database()
    log.info("Generating the initial data.")
    # This is where the database will be populated


@app.route('/')
def index():
    return 'Hello, World!'


def main():
    generate_data()
    app.run()


if __name__ == '__main__':
    main()
