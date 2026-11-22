import logging
from datetime import date, datetime

from pymongo import ASCENDING as ASC

log = logging.getLogger()

#colecciones 
def _ensure_collection(db, name):
    """Crea la colección si no existe."""
    if name not in db.list_collection_names():
        db.create_collection(name)

def create_routes(db):
    """Colección routes e índices 1, 2 y 3"""
    log.info("Asegurando colección routes")
    _ensure_collection(db, "routes")
    #Indice 1: identificador de ruta 
    db.routes.create_index([("route_id", ASC)], unique=True, name="idx_routes_route_id")
    #Indice 2: origen y destino de ruta 
    db.routes.create_index([("origin_station", ASC), ("destination_station", ASC)],
                           name="idx_routes_origin_destination")
    #Indice 3: estaciones dentro de la ruta
    db.routes.create_index([("stations.station_id", ASC)], name="idx_routes_stations_station_id")


def create_stations(db):
    """Colección stations e índice 4"""
    log.info("Asegurando colección stations")
    _ensure_collection(db, "stations")
    #Indice 4: identificador de estacion 
    db.stations.create_index([("station_id", ASC)], unique=True, name="idx_stations_station_id")


def create_schedules(db):
    """Colección schedules e índices 5 y 6"""
    log.info("Asegurando colección schedules")
    _ensure_collection(db, "schedules")
    #Indice 5: horarios por origen, destino, fecha y hora de salida
    db.schedules.create_index([("departure_station", ASC), ("arrival_station", ASC),
                               ("service_date", ASC), ("departure_time", ASC)],
                              name="idx_schedules_origin_dest_date_time")
    #Indice 6: horarios por tipo de transporte, estacion de salida, fecha y hora 
    db.schedules.create_index([("transport_type", ASC), ("departure_station", ASC),
                               ("service_date", ASC), ("departure_time", ASC)],
                              name="idx_schedules_type_station_date_time")


def setup_schema(db):
    """Crea las 3 colecciones. Es idempotente (puede ejecutarse n cantidad de veces sin que cambie el resultado)"""
    create_routes(db)
    create_stations(db)
    create_schedules(db)
