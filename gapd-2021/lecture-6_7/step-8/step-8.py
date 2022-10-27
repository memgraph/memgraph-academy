import json
import logging
import time
from argparse import ArgumentParser
from enum import Enum
from flask import Flask, render_template, Response
from functools import wraps
from gqlalchemy import Memgraph, Match
from random import randint, sample


log = logging.getLogger(__name__)


def init_log():
    logging.basicConfig(level=logging.DEBUG)
    log.info("Logging enabled")
    logging.getLogger("werkzeug").setLevel(logging.WARNING)


init_log()


def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        log.info(f"Time for {func.__name__} is {duration}")
        return result
    return wrapper


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


app = Flask(__name__,
            template_folder=args.template_folder,
            static_folder=args.static_folder,
            static_url_path='')


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
def init_data(card_count, pos_count):
    """Populate the database with initial Credit Card and POS device entries."""

    memgraph.execute_query("UNWIND range(0, {} - 1) AS id "
                           "CREATE (:Card {{id: id, compromised: false}})".format(
                               card_count))
    memgraph.execute_query("UNWIND range({}, {} - 1) AS id "
                           "CREATE (:Pos {{id: id, compromised: false}})".format(
                               card_count, card_count + pos_count))


def compromise_pos(pos_id):
    """Mark a POS device as compromised."""

    memgraph.execute_query(
        "MATCH (p:Pos {{id: {}}}) SET p.compromised = true".format(pos_id))
    log.info("Point of sale %d is compromised", pos_id)


@log_time
def compromise_pos_devices(card_count, pos_count, fraud_count):
    """Compromise a number of random POS devices."""

    log.info("Compromising {} out of {} POS devices".format(
        fraud_count, pos_count))

    compromised_devices = sample(
        range(card_count, card_count + pos_count), fraud_count)
    for pos_id in compromised_devices:
        compromise_pos(pos_id)


@log_time
def pump_transactions(card_count, pos_count, tx_count, report_pct):
    """Create transactions. If the POS device is compromised,
    then the card in the transaction gets compromised too.
    If the card is compromised, there is a 50% chance the
    transaction is fraudulent and detected (regardless of
    the POS device)."""

    log.info("Creating {} transactions".format(tx_count))

    query = ("MATCH (c:Card {{id: {}}}), (p:Pos {{id: {}}}) "
             "CREATE (t:Transaction "
             "{{id: {}, fraudReported: c.compromised AND (rand() < %f)}}) "
             "CREATE (c)<-[:Using]-(t)-[:At]->(p) "
             "SET c.compromised = p.compromised" % report_pct)

    def rint(min, max): return randint(min, max - 1)
    for i in range(card_count + pos_count, card_count + pos_count + tx_count):
        memgraph.execute_query(query.format(rint(0, card_count),
                                            rint(card_count,
                                                 card_count + pos_count),
                                            i))


@log_time
def generate_data():
    memgraph.drop_database()
    log.info("Generating the initial data.")

    number_of_pos = 10
    number_of_cards = 20
    number_of_transactions = 30
    number_of_compromised_pos = 2
    rate_of_fraudulent_transactions = 0.5

    # Create POS devices and Credit Cards
    init_data(number_of_cards,
              number_of_pos)

    # Compromise a number of those POS devices
    compromise_pos_devices(number_of_cards,
                           number_of_pos,
                           number_of_compromised_pos)

    # Create transactions and mark some of them a fraudulent
    pump_transactions(number_of_cards,
                      number_of_pos,
                      number_of_transactions,
                      rate_of_fraudulent_transactions)


class Properties(Enum):
    ID = "id"
    FRAUDREPORTED = "fraudReported"
    COMPROMISED = "compromised"


@log_time
@app.route('/get-graph', methods=['GET'])
def get_graph():
    log.info("Client fetching POS connected components")

    memgraph.execute_and_fetch("MATCH (pos:Pos)<-[:At]-(transaction:Transaction {fraudReported: false}) "
                               "RETURN pos, transaction")
    try:
        results = (
            Match()
            .node("Transaction", variable="transaction")
            .to("At")
            .node("Pos", variable="pos")
            .execute()
        )
        nodes_set = set()
        links_set = set()
        for result in results:
            pos_id = result["pos"].properties[Properties.ID.value]
            pos_label = "POS " + str(pos_id)
            pos_compromised = result["pos"].properties[Properties.COMPROMISED.value]

            transaction_id = result["transaction"].properties[Properties.ID.value]
            transaction_label = "Transaction " + str(transaction_id)
            transaction_fraudulent = result["transaction"].properties[Properties.FRAUDREPORTED.value]

            nodes_set.add((pos_id, pos_label, pos_compromised))
            nodes_set.add(
                (transaction_id, transaction_label, transaction_fraudulent))

            if (pos_id, transaction_id) not in links_set and (transaction_id, pos_id) not in links_set:
                links_set.add((transaction_id, pos_id))

        nodes = [
            {"id": node_id, "label": node_label, "fraud": node_fraud}
            for node_id, node_label, node_fraud in nodes_set
        ]
        links = [{"source": n_id, "target": m_id}
                 for (n_id, m_id) in links_set]

        response = {"nodes": nodes, "links": links}

        return Response(
            json.dumps(response),
            status=200,
            mimetype='application/json')

    except Exception as e:
        log.info("Data fetching went wrong.")
        log.info(e)
        return ("", 500)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


def main():
    generate_data()
    app.run(host=args.app_host, port=args.app_port, debug=args.debug)


if __name__ == '__main__':
    main()
