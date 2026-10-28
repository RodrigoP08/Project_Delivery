import logging
log = logging.getLogger()


CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS {}
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {} }}
"""

def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Asegurando que exista el keyspace: {keyspace} (RF={replication_factor})")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))
