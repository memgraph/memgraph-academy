import time
from flask import Flask
from gqlalchemy import Memgraph


app = Flask(__name__)


# Connect to a Memgraph instance
memgraph = Memgraph()
connection_established = False
while(not connection_established):
    try:
        if (memgraph._get_cached_connection().is_active()):
            connection_established = True
    except:
        time.sleep(4)


def generate_data():
    memgraph.drop_database()
    # This is where the database will be populated later on


@app.route('/')
def index():
    return 'Hello, World!'


def main():
    generate_data()
    app.run()


if __name__ == '__main__':
    main()
