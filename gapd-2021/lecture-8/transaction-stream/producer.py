import json
import logging
import os
import random
import stream_setup
from argparse import ArgumentParser
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from time import sleep


log = logging.getLogger(__name__)

KAFKA_HOST = os.getenv("KAFKA_HOST", "kafka")
KAFKA_PORT = os.getenv("KAFKA_PORT", "9092")
MEMGRAPH_HOST = os.getenv("MEMGRAPH_HOST", "memgraph-mage")
MEMGRAPH_PORT = int(os.getenv("MEMGRAPH_PORT", "7687"))


def init_log():
    logging.basicConfig(level=logging.DEBUG)
    log.info("Logging enabled")


def parse_args():
    """
    Parse input command line arguments.
    """
    parser = ArgumentParser(
        description="A credit card transaction stream machine powered by Memgraph.")
    parser.add_argument(
        "--interval",
        type=int,
        help="Interval for sending data in seconds.")
    return parser.parse_args()


def create_kafka_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_HOST + ':' + KAFKA_PORT)
            return producer
        except NoBrokersAvailable:
            log.info("Failed to connect to Kafka")
            sleep(1)


def create_transaction(card_count, pos_count, report_pct, cnt):
    def rint(min, max): return random.randint(min, max - 1)
    new_transaction = {
        'card_id': rint(0, card_count),
        'pos_id':  rint(card_count, card_count + pos_count),
        'transaction_id': cnt,
        'compromised': random.uniform(0, 1) > report_pct
    }

    return new_transaction


def main():
    init_log()
    args = parse_args()

    stream_setup.create_topic(KAFKA_HOST, KAFKA_PORT)
    memgraph = stream_setup.connect_to_memgraph(MEMGRAPH_HOST, MEMGRAPH_PORT)
    stream_setup.create_stream(memgraph)

    producer = create_kafka_producer()

    number_of_pos = 10
    number_of_cards = 20
    rate_of_fraudulent_transactions = 0.5
    cnt = 1000

    while(True):
        # Create transactions and mark some of them a fraudulent
        transaction = create_transaction(number_of_cards,
                                         number_of_pos,
                                         rate_of_fraudulent_transactions,
                                         cnt)
        cnt = cnt + 1
        producer.send("transactions", json.dumps(transaction).encode('utf8'))
        sleep(args.interval)


if __name__ == "__main__":
    main()
