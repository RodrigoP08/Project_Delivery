import logging
from datetime import datetime
from cassandra.util import Date
log = logging.getLogger()

CREATE_KEYSPACE = """
    CREATE KEYSPACE IF NOT EXISTS {}
    WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {} }}
"""

CREATE_TRIPS_BY_USER = """
    CREATE TABLE IF NOT EXISTS trips_by_user (
        user_id TEXT,
        start_time TIMESTAMP,
        trip_id TEXT,
        route_id TEXT,
        start_station TEXT,
        end_station TEXT,
        end_time TIMESTAMP,
        PRIMARY KEY ((user_id), start_time, trip_id)
    ) WITH CLUSTERING ORDER BY (start_time DESC, trip_id ASC)
"""

INSERT_TRIPS_BY_USER = """
    INSERT INTO trips_by_user (user_id, start_time, trip_id, route_id, start_station, end_station, end_time)
    VALUES(?,?,?,?,?,?,?)
"""


CREATE_TRIPS_BY_ROUTE = """
    CREATE TABLE IF NOT EXISTS trips_by_route (
        route_id TEXT,
        trip_date DATE,
        start_time TIMESTAMP,
        trip_id TEXT,
        transport_id TEXT,
        end_time TIMESTAMP,
        passenger_count INT,
        PRIMARY KEY ((route_id, trip_date), start_time, trip_id)
    ) WITH CLUSTERING ORDER BY (start_time DESC, trip_id ASC)
"""

INSERT_TRIPS_BY_ROUTE = """
    INSERT INTO trips_by_route (route_id, trip_date, start_time, trip_id, transport_id, end_time, passenger_count)
    VALUES(?,?,?,?,?,?,?)
"""
CREATE_STOPS_USER_TRIP = """
    CREATE TABLE IF NOT EXISTS stops_user_trip (
        user_id TEXT,
        trip_id TEXT,
        stop_sequence INT,
        station_id TEXT,
        station_name TEXT,
        arrival_time TIMESTAMP,
        PRIMARY KEY ((user_id, trip_id), stop_sequence)
    ) WITH CLUSTERING ORDER BY (stop_sequence ASC)
"""
INSERT_STOPS_USER_TRIP = """
    INSERT INTO stops_user_trip (user_id, trip_id, stop_sequence, station_id, station_name, arrival_time)
    VALUES(?,?,?,?,?,?)
"""

CREATE_TRIPS_TRANSPORT_DAY = """
    CREATE TABLE IF NOT EXISTS trips_transport_day (
        transport_id TEXT,
        service_date DATE,
        departure_time TIMESTAMP,
        trip_id TEXT,
        route_id TEXT,
        start_station TEXT,
        arrival_time TIMESTAMP,
        passenger_count INT,
        PRIMARY KEY ((transport_id, service_date), departure_time, trip_id)
    ) WITH CLUSTERING ORDER BY (departure_time ASC, trip_id ASC)
"""
INSERT_TRIPS_TRANSPORT_DAY = """
    INSERT INTO trips_transport_day (transport_id, service_date, departure_time, trip_id, route_id, start_station, arrival_time, passenger_count)
    VALUES(?,?,?,?,?,?,?,?)
"""

CREATE_USE_ROUTE_PER_HOUR = """
    CREATE TABLE IF NOT EXISTS use_route_per_hour (
        route_id TEXT,
        usage_date DATE,
        hour INT,
        passenger_count INT,
        PRIMARY KEY ((route_id, usage_date), hour)
    ) WITH CLUSTERING ORDER BY (hour ASC)
"""
INSERT_USE_ROUTE_PER_HOUR = """
    INSERT INTO use_route_per_hour (route_id, usage_date, hour, passenger_count)
    VALUES(?,?,?,?)
"""

CREATE_STOPS_USER = """
    CREATE TABLE IF NOT EXISTS stops_user (
        user_id TEXT,
        route_id TEXT,
        start_time TIMESTAMP,
        trip_id TEXT,
        start_station TEXT,
        end_station TEXT,
        PRIMARY KEY ((user_id, route_id), start_time, trip_id)
    ) WITH CLUSTERING ORDER BY (start_time DESC, trip_id ASC)
"""

INSERT_STOPS_USER = """
    INSERT INTO stops_user (user_id, route_id, start_time, trip_id, start_station, end_station)
    VALUES(?,?,?,?,?,?)
"""

# Req 1: últimos 5 viajes de un usuario (start_time DESC, así que LIMIT 5 basta)
SELECT_LAST_5_TRIPS_FROM_USER = """
    SELECT trip_id, route_id, start_station, end_station, start_time, end_time
    FROM trips_by_user
    WHERE user_id = ?
    LIMIT 5
"""

# Req 2: viajes por ruta (en una fecha)
SELECT_TRIPS_BY_ROUTE = """
    SELECT trip_id, start_time, end_time, transport_id, passenger_count
    FROM trips_by_route
    WHERE route_id = ? AND trip_date = ?
"""

# Req 3: estaciones recorridas por un usuario en un viaje
SELECT_STOPS_USER_TRIP = """
    SELECT stop_sequence, station_id, station_name, arrival_time
    FROM stops_user_trip
    WHERE user_id = ? AND trip_id = ?
"""


# Req 4: hora de inicio de la ruta de un transporte (primer viaje del día, orden ASC)
SELECT_FIRST_DEPARTURE_TRANSPORT = """
    SELECT departure_time, route_id, trip_id
    FROM trips_transport_day
    WHERE transport_id = ? AND service_date = ?
    LIMIT 1
"""

# Req 5: uso de ruta por hora (toda la fecha, o una hora específica)
SELECT_ROUTE_USAGE_BY_DAY = """
    SELECT hour, passenger_count
    FROM use_route_per_hour
    WHERE route_id = ? AND usage_date = ?
"""
SELECT_ROUTE_USAGE_AT_HOUR = """
    SELECT hour, passenger_count
    FROM use_route_per_hour
    WHERE route_id = ? AND usage_date = ? AND hour = ?
"""

# Req 6: viajes de un usuario en un rango de fechas
SELECT_USER_TRIPS_IN_RANGE = """
    SELECT trip_id, route_id, start_station, end_station, start_time, end_time
    FROM trips_by_user
    WHERE user_id = ? AND start_time >= ? AND start_time <= ?
"""

# Req 7: historial de recorridos de un transporte (en un día)
SELECT_TRANSPORT_HISTORY = """
    SELECT departure_time, arrival_time, trip_id, route_id, start_station, passenger_count
    FROM trips_transport_day
    WHERE transport_id = ? AND service_date = ?
"""

# Req 8: viajes de un usuario en una ruta específica
SELECT_USER_TRIPS_ON_ROUTE = """
    SELECT trip_id, start_time, start_station, end_station
    FROM stops_user
    WHERE user_id = ? AND route_id = ?
"""


def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Asegurando que exista el keyspace: {keyspace} (RF={replication_factor})")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))
    session.set_keyspace(keyspace)   # importante para que las tablas se creen ahí

def create_schema(session):
    log.info("CREANDO O ASEGURANDO TABLAS DE CASSANDRA")
    session.execute(CREATE_TRIPS_BY_USER)
    session.execute(CREATE_TRIPS_BY_ROUTE)
    session.execute(CREATE_STOPS_USER_TRIP)
    session.execute(CREATE_USE_ROUTE_PER_HOUR)
    session.execute(CREATE_STOPS_USER)
    session.execute(CREATE_TRIPS_TRANSPORT_DAY)
    
def get_last_5_trips(session, user_id):
    stmt = session.prepare(SELECT_LAST_5_TRIPS_FROM_USER)
    rows = session.execute(stmt, [user_id])

    print(f"\n=== Últimos 5 viajes del usuario: {user_id} ===")
    for row in rows:
        print(f"Viaje: {row.trip_id}")
        print(f"  - Ruta: {row.route_id}")
        print(f"  - Estación inicio: {row.start_station}")
        print(f"  - Estación fin: {row.end_station}")
        print(f"  - Inicio: {row.start_time:%Y-%m-%d %H:%M}")
        print(f"  - Fin: {row.end_time:%Y-%m-%d %H:%M}")
        print()


def get_trips_by_route(session, route_id, trip_date):
    stmt = session.prepare(SELECT_TRIPS_BY_ROUTE)
    rows = session.execute(stmt, [route_id, trip_date])

    print(f"\n=== Viajes de la ruta {route_id} el {trip_date} ===")
    for row in rows:
        print(f"Viaje: {row.trip_id}")
        print(f"  - Transporte: {row.transport_id}")
        print(f"  - Inicio: {row.start_time:%H:%M}")
        print(f"  - Fin: {row.end_time:%H:%M}")
        print(f"  - Pasajeros: {row.passenger_count}")
        print()


def get_stops_user_trip(session, user_id, trip_id):
    stmt = session.prepare(SELECT_STOPS_USER_TRIP)
    rows = session.execute(stmt, [user_id, trip_id])

    print(f"\n=== Estaciones del viaje {trip_id} (usuario {user_id}) ===")
    for row in rows:
        print(f"Parada #{row.stop_sequence}")
        print(f"  - Estación: {row.station_name} ({row.station_id})")
        print(f"  - Llegada: {row.arrival_time:%H:%M}")
        print()


def get_first_departure(session, transport_id, service_date):
    stmt = session.prepare(SELECT_FIRST_DEPARTURE_TRANSPORT)
    row = session.execute(stmt, [transport_id, service_date]).one()

    print(f"\n=== Hora de inicio del transporte {transport_id} el {service_date} ===")
    if row is None:
        print("No se encontraron viajes.")
        return
    print(f"  - Hora de inicio: {row.departure_time:%H:%M}")
    print(f"  - Ruta: {row.route_id}")
    print(f"  - Viaje: {row.trip_id}")
    print()


def get_route_usage(session, route_id, usage_date, hour=None):
    log.info(f" usage for route: {route_id} on {usage_date}")
    if hour is None:
        stmt = session.prepare(SELECT_ROUTE_USAGE_BY_DAY)
        rows = session.execute(stmt, [route_id, usage_date])
    else:
        stmt = session.prepare(SELECT_ROUTE_USAGE_AT_HOUR)
        rows = session.execute(stmt, [route_id, usage_date, hour])

    print(f"\n=== Uso de la ruta {route_id} el {usage_date} ===")
    for row in rows:
        print(f"Hora {row.hour:02d}:00")
        print(f"  - Pasajeros: {row.passenger_count}")
        print()


def get_user_trips_in_range(session, user_id, start, end):
    stmt = session.prepare(SELECT_USER_TRIPS_IN_RANGE)
    rows = session.execute(stmt, [user_id, start, end])

    print(f"\n=== Viajes de {user_id} entre {start:%Y-%m-%d} y {end:%Y-%m-%d} ===")
    for row in rows:
        print(f"Viaje: {row.trip_id}")
        print(f"  - Ruta: {row.route_id}")
        print(f"  - Estación inicio: {row.start_station}")
        print(f"  - Estación fin: {row.end_station}")
        print(f"  - Inicio: {row.start_time:%Y-%m-%d %H:%M}")
        print(f"  - Fin: {row.end_time:%Y-%m-%d %H:%M}")
        print()


def get_transport_history(session, transport_id, service_date):
    stmt = session.prepare(SELECT_TRANSPORT_HISTORY)
    rows = session.execute(stmt, [transport_id, service_date])

    print(f"\n=== Historial del transporte {transport_id} el {service_date} ===")
    for row in rows:
        print(f"Viaje: {row.trip_id}")
        print(f"  - Ruta: {row.route_id}")
        print(f"  - Estación inicio: {row.start_station}")
        print(f"  - Salida: {row.departure_time:%H:%M}")
        print(f"  - Llegada: {row.arrival_time:%H:%M}")
        print(f"  - Pasajeros: {row.passenger_count}")
        print()


def get_user_trips_on_route(session, user_id, route_id):
    log.info(f"Retrieving trips for user: {user_id} on route: {route_id}")
    stmt = session.prepare(SELECT_USER_TRIPS_ON_ROUTE)
    rows = session.execute(stmt, [user_id, route_id])

    print(f"\n=== Viajes de {user_id} en la ruta {route_id} ===")
    for row in rows:
        print(f"Viaje: {row.trip_id}")
        print(f"  - Inicio: {row.start_time:%Y-%m-%d %H:%M}")
        print(f"  - Estación inicio: {row.start_station}")
        print(f"  - Estación fin: {row.end_station}")
        print()