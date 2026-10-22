#!/usr/bin/env python3
# import falcon.asgi NO SE BIEN SI SE NECESITA AUN
import os
import sys

import logging

from pymongo import MongoClient
from cassandra.cluster import Cluster


CASSANDRA_IPS = os.getenv("CASSANDRA_CLUSTER_IPS", "127.0.0.1").split(",")
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", "9042"))
CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "transporte")
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")


def setup_logging():
    # PARA PODER LLEVAR UN REGISTRO DE QUE PASA USAREMOS LOGS
    os.makedirs(LOG_DIR, exist_ok=True)
    
    log = logging.getLogger()
    log.setLevel('INFO')
    handler = logging.FileHandler(LOG_FILE)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    log.addHandler(handler)
    
 
setup_logging()
log = logging.getLogger("connect")

def connect_cassandra():
    log.info("Conectando a Cassandra: %s:%s", CASSANDRA_IPS, CASSANDRA_PORT)
    try:
        cluster = Cluster(CASSANDRA_IPS, port=CASSANDRA_PORT)
        session = cluster.connect()
        session.set_keyspace(CASSANDRA_KEYSPACE)
        log.info("Cassandra conectado. Keyspace: %s", CASSANDRA_KEYSPACE)
        return session
    except Exception as e:
        log.error("Error crítico al intentar conectar a Cassandra: %s", e)
        raise e
