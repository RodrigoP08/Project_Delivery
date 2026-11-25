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

def _day(value):
    """'YYYY-MM-DD'datetime -> datetime a medianoche, o sea como se guarda service_date."""
    if isinstance(value, datetime):
        return value.replace(hour=0, minute=0, second=0, microsecond=0)
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day)
    return datetime.strptime(str(value), "%Y-%m-%d")


def print_docs(docs, limit=30):
    """Imprime una lista de documentos, una línea por documento"""
    if not docs:
        print("  No se encontraron resultados.")
        return
    if isinstance(docs, dict):
        docs = [docs]
    for i, doc in enumerate(docs[:limit], start=1):
        parts = []
        for key, value in doc.items():
            if isinstance(value, datetime):
                value = value.strftime("%Y-%m-%d %H:%M")
            parts.append(f"{key}: {value}")
        print(f"  {i:>2}. " + " | ".join(parts))
    if len(docs) > limit:
        print(f"  ... y {len(docs) - limit} más (total: {len(docs)})")
    else:
        print(f"\n  Total: {len(docs)}")


SCHEDULE_FIELDS = {"_id": 0, "transport_id": 1, "transport_type": 1, "route_id": 1,
                   "departure_station": 1, "arrival_station": 1,
                   "departure_time": 1, "arrival_time": 1}

ROUTE_FIELDS = {"_id": 0, "route_id": 1, "route_name": 1, "origin_station": 1,
                "destination_station": 1, "transport_type": 1, "estimated_duration": 1}


#CONSULTAS
#cada consulta imprime el resultado

#Req 1: horarios entre dos estaciones
def get_schedules_between_stations(db, origin, destination, service_date):
    docs = list(db.schedules.find(
        {"departure_station": origin, "arrival_station": destination,
         "service_date": _day(service_date)},
        SCHEDULE_FIELDS).sort("departure_time", 1))    #indice 5
    print(f"\n=== Horarios de {origin} a {destination} el {service_date} ===")
    print_docs(docs)
    return docs


#Req 2: rutas entre estaciones
def get_routes_between_stations(db, origin, destination, include_intermediate=False):
    if not include_intermediate:
        #indice 2
        docs = list(db.routes.find(
            {"origin_station": origin, "destination_station": destination}, ROUTE_FIELDS))
    else:
        #indice 3
        docs = []
        for route in db.routes.find({"stations.station_id": {"$all": [origin, destination]}}):
            order = {s["station_id"]: s["stop_sequence"] for s in route["stations"]}
            if order[origin] < order[destination]:
                docs.append({k: route[k] for k in ROUTE_FIELDS if k != "_id"})
    print(f"\n=== Rutas de {origin} a {destination} "
          f"({'con paradas intermedias' if include_intermediate else 'extremo a extremo'}) ===")
    print_docs(docs)
    return docs


#Req 3: información de una estación
def get_station_info(db, station_id):
    doc = db.stations.find_one(
        {"station_id": station_id},
        {"_id": 0, "station_id": 1, "station_name": 1,
         "transport_types": 1, "route_ids": 1})       #indice 4
    print(f"\n=== Información de la estación {station_id} ===")
    print_docs(doc)
    return doc


#Req 4: horarios por tipo de transporte y estación
def get_schedules_by_type_and_station(db, transport_type, station_id, service_date):
    docs = list(db.schedules.find(
        {"transport_type": transport_type, "departure_station": station_id,
         "service_date": _day(service_date)},
        SCHEDULE_FIELDS).sort("departure_time", 1))     #indice 6
    print(f"\n=== Salidas de {transport_type} desde {station_id} el {service_date} ===")
    print_docs(docs)
    return docs


#Req 5: rutas agrupadas por duración estimada
DURATION_CATEGORIES = ["15 minutos", "30 minutos", "Más de 30 minutos"]

def get_routes_by_duration(db):
    """<=15 min, 16-30 min y >30 min. Siempre devuelve las 3 categorías y 0 si no hay rutas"""
    pipeline = [
        {"$group": {
            "_id": {"$switch": {
                "branches": [
                    {"case": {"$lte": ["$estimated_duration", 15]}, "then": DURATION_CATEGORIES[0]},
                    {"case": {"$lte": ["$estimated_duration", 30]}, "then": DURATION_CATEGORIES[1]},
                ],
                "default": DURATION_CATEGORIES[2],
            }},
            "total_routes": {"$sum": 1},
        }},
        {"$group": {"_id": None, "counts": {"$push": {"k": "$_id", "v": "$total_routes"}}}},
        {"$project": {"_id": 0, "categories": {"$map": {
            "input": DURATION_CATEGORIES, "as": "cat",
            "in": {
                "duration_category": "$$cat",
                "total_routes": {"$ifNull": [{"$arrayElemAt": [
                    {"$map": {
                        "input": {"$filter": {"input": "$counts", "cond": {"$eq": ["$$this.k", "$$cat"]}}},
                        "in": "$$this.v"}},
                    0]}, 0]},
            }}}}},
        {"$unwind": "$categories"},
        {"$replaceRoot": {"newRoot": "$categories"}},
    ]
    docs = list(db.routes.aggregate(pipeline))
    print("\n=== Rutas agrupadas por duración estimada ===")
    print_docs(docs)
    return docs


#Req 6: transportes disponibles en una estación 
def get_transports_in_station(db, station_id):
    pipeline = [
        {"$match": {"stations.station_id": station_id}},     #indice 3
        {"$group": {"_id": "$transport_type", "route_ids": {"$push": "$route_id"}}},
        {"$addFields": {"station_id": station_id}},
        {"$lookup": {"from": "stations", "localField": "station_id",
                     "foreignField": "station_id", "as": "station"}},    #indice 4
        {"$unwind": "$station"},
        {"$project": {"_id": 0, "station_id": 1, "station_name": "$station.station_name",
                      "transport_type": "$_id", "route_ids": 1}},
        {"$sort": {"transport_type": 1}},
    ]
    docs = list(db.routes.aggregate(pipeline))
    print(f"\n=== Transportes disponibles en la estación {station_id} ===")
    print_docs(docs)
    return docs


#Req 7: cantidad de estaciones por ruta AGREGACION 1
def get_stations_per_route(db):
    docs = list(db.routes.aggregate([
        {"$unwind": "$stations"},
        {"$group": {"_id": "$route_id", "route_name": {"$first": "$route_name"},
                    "total_stations": {"$sum": 1}}},
        {"$sort": {"total_stations": -1, "_id": 1}},
        {"$project": {"_id": 0, "route_id": "$_id", "route_name": 1, "total_stations": 1}},
    ]))
    print("\n=== Cantidad de estaciones por ruta ===")
    print_docs(docs)
    return docs


#Req 8: cantidad de rutas por tipo de transporte AGREGACION 2
def get_routes_per_transport_type(db):
    docs = list(db.routes.aggregate([
        {"$group": {"_id": "$transport_type", "total_routes": {"$sum": 1}}},
        {"$sort": {"total_routes": -1, "_id": 1}},
        {"$project": {"_id": 0, "transport_type": "$_id", "total_routes": 1}},
    ]))
    print("\n=== Cantidad de rutas por tipo de transporte ===")
    print_docs(docs)
    return docs



def explain_query(db, collection, filter_, sort=None):
    """Muestra qué índice usó MongoDB en un find (explain)."""
    cmd = {"find": collection, "filter": filter_}
    if sort:
        cmd["sort"] = sort
    result = db.command("explain", cmd, verbosity="executionStats")

    plan = result["queryPlanner"]["winningPlan"]
    plan = plan.get("queryPlan", plan)       
    while "inputStage" in plan:             
        plan = plan["inputStage"]

    stats = result["executionStats"]
    print(f"  Etapa:    {plan['stage']}")     #IXSCAN = índice, COLLSCAN = sin índice
    print(f"  Índice:   {plan.get('indexName', 'ninguno')}")
    print(f"  Documentos revisados: {stats['totalDocsExamined']} | devueltos: {stats['nReturned']}")


def list_stations(db):
    return list(db.stations.find({}, {"_id": 0, "station_id": 1, "station_name": 1}).sort("station_id", 1))


def list_transport_types(db):
    return sorted(db.routes.distinct("transport_type"))