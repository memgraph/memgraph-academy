import logging
import time
from gqlalchemy import Memgraph
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, NoBrokersAvailable


log = logging.getLogger(__name__)


def connect_to_memgraph(memgraph_host, memgraph_port):
    memgraph = Memgraph(memgraph_host, memgraph_port)
    connection_established = False
    while(not connection_established):
        try:
            if (memgraph._get_cached_connection().is_active()):
                connection_established = True
                log.info("Connected to Memgraph")
        except:
            log.info("Memgraph probably isn't running")
            time.sleep(4)
    return memgraph


def create_stream(memgraph):
    try:
        log.info("Creating stream connections on Memgraph")
        memgraph.execute(
            "CREATE STREAM transaction_stream TOPICS transactions TRANSFORM card_fraud.transaction")
        memgraph.execute("START STREAM transaction_stream")
        log.info("Stream creation succeed")
    except:
        log.info("Stream creation failed or streams already exist")


def get_admin_client(kafka_ip, kafka_port):
    while True:
        try:
            admin_client = KafkaAdminClient(
                bootstrap_servers=kafka_ip + ':' + kafka_port,
                client_id="transaction_stream")
            return admin_client
        except NoBrokersAvailable:
            log.info("Failed to connect to Kafka")
            time.sleep(1)


def create_topic(kafka_ip, kafka_port):
    admin_client = get_admin_client(kafka_ip, kafka_port)
    log.info("Connected to Kafka")

    topic_list = [
        NewTopic(
            name="transactions",
            num_partitions=1,
            replication_factor=1)]

    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except TopicAlreadyExistsError:
        pass
    log.info("Created topics")
