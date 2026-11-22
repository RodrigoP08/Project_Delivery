# Cassandra: CSV, las tablas son planas (una fila por evento), así que un CSV es ideal. 
# MongoDB: JSON, MongoDB ya utiliza este formato por lo que es forma facil de manipulación. 
# Dgraph: JSON, usaremos un JSON porque puede representar fácilmente las relaciones (objetos dentro de otros objetos) 

'''
La idea es que se tenga un archivo de los mencionados anteriormente en la carpeta data/ en la cual
se buscara la manera de extraer los datos de cada uno y realizar la poblacion de cada base de datos
'''
import csv, os, json
from datetime import datetime

from connect import log
from Cassandra import model_Cassandra


#*********************************************************************************************
def to_TIMESTAMP(v): 
    #convertir a datetime
    return datetime.strptime(v, "%Y-%m-%d %H:%M:%S%z")
def to_DATE(v):      
    #convertir a date
    return datetime.strptime(v[:10], "%Y-%m-%d").date()

def leer_csv(nombre):
    with open(f"data/{nombre}.csv", mode="r", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def poblar_trips_by_user(session):
    stmt = session.prepare(model_Cassandra.INSERT_TRIPS_BY_USER)
    for f in leer_csv("trips_by_user"):
        session.execute(stmt, (
            f['user_id'], to_TIMESTAMP(f['start_time']), f['trip_id'], f['route_id'],
            f['start_station'], f['end_station'], to_TIMESTAMP(f['end_time'])
        ))
def poblar_trips_by_route(session):
    stmt = session.prepare(model_Cassandra.INSERT_TRIPS_BY_ROUTE)
    for f in leer_csv("trips_by_route"):
        session.execute(stmt, (
            f['route_id'], to_DATE(f['trip_date']), to_TIMESTAMP(f['start_time']), f['trip_id'],
            f['transport_id'], to_TIMESTAMP(f['end_time']), int(f['passenger_count'])
        ))
        
def poblar_stops_user_trip(session):
    stmt = session.prepare(model_Cassandra.INSERT_STOPS_USER_TRIP)
    for f in leer_csv("stops_user_trip"):
        session.execute(stmt, (
            f['user_id'], f['trip_id'], int(f['stop_sequence']),
            f['station_id'], f['station_name'], to_TIMESTAMP(f['arrival_time'])
        ))

def poblar_use_route_per_hour(session):
    stmt = session.prepare(model_Cassandra.INSERT_USE_ROUTE_PER_HOUR)
    for f in leer_csv("use_route_per_hour"):
        session.execute(stmt, (
            f['route_id'], to_DATE(f['usage_date']), to_TIMESTAMP(f['hour']).hour,
            int(f['passenger_count'])
        ))

def poblar_stops_user(session):
    stmt = session.prepare(model_Cassandra.INSERT_STOPS_USER)
    for f in leer_csv("stops_user"):
        session.execute(stmt, (
            f['user_id'], f['route_id'], to_TIMESTAMP(f['start_time']), f['trip_id'],
            f['start_station'], f['end_station']
        ))

def poblar_trips_transport_day(session):
    stmt = session.prepare(model_Cassandra.INSERT_TRIPS_TRANSPORT_DAY)
    for f in leer_csv("trips_transport_day"):
        session.execute(stmt, (
            f['transport_id'], to_DATE(f['service_date']), to_TIMESTAMP(f['departure_time']),
            f['trip_id'], f['route_id'], f['start_station'],
            to_TIMESTAMP(f['arrival_time']), int(f['passenger_count'])
        ))
        
def poblar_cassandra(session):
    poblar_trips_by_user(session)
    poblar_trips_by_route(session)
    poblar_stops_user_trip(session)
    poblar_trips_transport_day(session)
    poblar_use_route_per_hour(session)
    poblar_stops_user(session)
    log.info("Cassandra poblada")

#************************************************************************************************************

# def poblar_datos(mongo_db, cassandra_session, dgraph_client):
def poblar_datos(cassandra_session):
    if cassandra_session is not None:
        poblar_cassandra(cassandra_session)
        
    print("Poblado de datos terminado.")