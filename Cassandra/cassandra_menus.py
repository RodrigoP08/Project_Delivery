import os
import sys
from datetime import datetime, timedelta


# Obtiene la ruta de la carpeta actual y sube un nivel hacia la raíz del proyecto
ruta_raiz = os.path.abspath( os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ruta_raiz)
from connect import log 

from Cassandra import model_Cassandra

def print_menu_cassandra():
    mm_options = {
        0: "EXIT",
        1: "Ultimos 5 viajes de un usuario",
        2: "Viajes realizados por una ruta",
        3: "Estaciones recorridas por un usuario en un viaje especifico",
        4: "Hora de inicio de la ruta de un transporte",
        5: "Uso de ruta por hora",
        6: "Viajes de un usuario en un rango de fechas",
        7: "Historial de recorridos de un transporte",
        8: "Viajes de un usuario en una ruta especifica"
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])

def actions_cassandra(session):
      while(True):
            print("\n" + "="*50)
            print_menu_cassandra()
            try:
                option = int(input('\nEnter your choice: '))
            except ValueError:
                print("Please enter a valid number.")
                continue
            try:
                if option == 0:
                    print(f"\nExiting...")
                    break
        
                elif option == 1:
                    print(f"\nQ1: Ultimos 5 viajes de un usuario")
                    # model.function_example(session)
                    user_id = input("user_id: ")
                    model_Cassandra.get_last_5_trips(session, user_id)
        
                elif option == 2:
                    print(f"\nQ2: Viajes realizados por ruta")
                    route_id = input("route_id: ")
                    trip_date = input("trip_date(YYY-MM-DD): ")
                    model_Cassandra.get_trips_by_route(session, route_id, trip_date)
                    
        
                elif option == 3:
                    print(f"\nQ3: Estaciones recorridas por un usuario en un viaje especifico")
                    user_id = input("user_id: ")
                    trip_id = input("trip_id: ")
                    model_Cassandra.get_stops_user_trip(session, user_id, trip_id)
        
                elif option == 4:
                    print(f"\nQ4: Hora de inicio de la ruta de un transporte")
                    transport_id = input("transport_id: ")
                    service_date = input("service_date: ")
                    model_Cassandra.get_first_departure(session, transport_id, service_date)
        
                elif option == 5:
                    print(f"\nQ5: Uso de ruta por hora")
                    route_id = input("route_id: ")
                    usage_date = input("usage_date: ")
                    hour_in = input("hour (0-23, vacío = todo el día): ").strip()
                    hour = int(hour_in) if hour_in else None
                    model_Cassandra.get_route_usage(session, route_id, usage_date, hour)
        
                elif option == 6:
                    print(f"\nQ6:Viajes de un usuario en un rango de fechas")
                    user_id = input("user_id: ")
                    start = datetime.strptime(input("start (YYYY-MM-DD): "), "%Y-%m-%d")
                    end = datetime.strptime(input("end (YYYY-MM-DD): "), "%Y-%m-%d") + timedelta(days=1)
                    model_Cassandra.get_user_trips_in_range(session, user_id, start, end)
        
                elif option == 7:
                    print(f"\nQ7: Historial de recorridos de un transporte")
                    transport_id = input("transport_id: ")
                    service_date = input("service_date: ")
                    model_Cassandra.get_transport_history(session, transport_id, service_date)
                        
                elif option == 8:
                    print(f"\nQ8: Viajes de un usuario en una ruta especifica")
                    user_id = input("user_id: ")
                    route_id = input("route_id: ")
                    model_Cassandra.get_user_trips_on_route(session, user_id, route_id)
                else:
                    print("Invalid option. Please try again.")
            except Exception as e:
                log.error("Error en consulta CASSANDRA (opcion %s): %s", option, e)
                print(f"Error al ejecutar la consulta: {e}")
                