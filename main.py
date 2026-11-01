
from connect import setup_logging, connect_cassandra, connect_mongo, connect_dgraph,log, sys

# from Cassandra import model


log = setup_logging()
def print_main_menu():
    menu = '''
    Análisis de Redes de Transporte
    1. Poblar todas las bases de datos
    2. (MongoDB)    Informacion de rutas, estaciones, horarios, y metadatos
    3. (Dgraph)     Relaciones entre estaciones, rutas y conexiones
    4. (Cassandra)  Historial de viajes
    5. EXIT
    '''
    print(menu)
    
def print_menu_cassandra():
    #MENY DE QUERYS
    #ESPERAR CONFIRMACION DEL KICK OFF
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
    #NO SE SI ESTA BIEN LA LOGICA SALUDOS
      while(True):
            print("\n" + "="*50)
            print_menu_cassandra()
            try:
                option = int(input('\nEnter your choice: '))
            except ValueError:
                print("Please enter a valid number.")
                continue
    
            if option == 0:
                print(f"\nExiting...")
                break
    
            elif option == 1:
                print(f"\nQ1: Ultimos 5 viajes de un usuario")
                # model.function_example(session)
    
            elif option == 2:
                print(f"\nQ2: Viajes realizados por ruta")
    
            elif option == 3:
                print(f"\nQ3: Estaciones recorridas por un usuario en un viaje especifico")
    
            elif option == 4:
                print(f"\nQ4: Hora de inicio de la ruta de un transporte")
    
            elif option == 5:
                print(f"\nQ5: Uso de ruta por hora")
    
            elif option == 6:
                print(f"\nQ6:Viajes de un usuario en un rango de fechas")
    
            elif option == 7:
                print(f"\nQ7: Historial de recorridos de un transporte")
                    
            elif option == 8:
                print(f"\nQ8: Viajes de un usuario en una ruta especifica")
            else:
                print("Invalid option. Please try again.")


def print_menu_mongo():
    mm_options = {
        0: "EXIT",
        1: "Consulta de horarios entre dos estaciones",
        2: "Consulta de rutas entre estaciones",
        3: "Consulta de informacion de una estacion",
        4: "Consulta de horarios por tipo de transporte y estacion",
        5: "Consulta de rutas agrupadas por duracion estimada",
        6: "Consulta de transportes disponibles en una estacion",
        7: "Consultar la cantidad de estaciones por ruta",
        8: "Consultar la cantidad de rutas por tipo de transporte",
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])

#preguntar por la estacion
def ask_station(label):
    return input(f"{label} (ej. ST001): ").strip().upper()

#obtener fecha 
def ask_date():
    pass

def actions_mongo(db):
    while(True):
        print("\n" + "="*50)
        print_menu_mongo()
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
                print(f"\nQ1: Consulta de horarios entre dos estaciones")

            elif option == 2:
                print(f"\nQ2: Consulta de rutas entre estaciones")

            elif option == 3:
                print(f"\nQ3: Consulta de informacion de una estacion")

            elif option == 4:
                print(f"\nQ4: Consulta de horarios por tipo de transporte y estacion")

            elif option == 5:
                print(f"\nQ5: Consulta de rutas agrupadas por duracion estimada")

            elif option == 6:
                print(f"\nQ6: Consulta de transportes disponibles en una estacion")
                
            elif option == 7:
                print(f"\nQ7: Cantidad de estaciones por ruta")

            elif option == 8:
                print(f"\nQ8: Cantidad de rutas por tipo de transporte")

            else:
                print("Invalid option. Please try again.")
        except Exception as e:
            log.error("Error en consulta MongoDB (opcion %s): %s", option, e)
            print(f"Error al ejecutar la consulta: {e}")

def print_menu_dgraph():
    mm_options = {
        0: "EXIT",
        1: "Calcular camino más corto entre dos estaciones por medio de las distancias.",
        2: "Mostrar y consultar estaciones adyacentes a una estación.",
        3: "Identificar las estaciones con mayor número de pasajeros.",
        4: "Mostrar estaciones donde se puede transbordar a otra línea de transporte.",
        5: "Determinar la validez de un camino.",
        6: "Encontrar rutas alcanzables por una determinada cantidad de saltos dentro del grafo.",
        7: "Buscar rutas alternativas con un transbordo.",
        8: "Mostrar todas las estaciones relacionadas a una línea.",
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])

def actions_dgraph(db):
    while(True):
        print("\n" + "="*50)
        print_menu_dgraph()
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
                print(f"\nQ1: Consulta el camino más corto entre dos estaciones por medio de las distancias.")

            elif option == 2:
                print(f"\nQ2: Consulta de estaciones adyacentes a una estación.")

            elif option == 3:
                print(f"\nQ3: Consulta de las estaciones con mayor número de pasajeros.")

            elif option == 4:
                print(f"\nQ4: Consulta de estaciones donde se puede transbordar a otra línea de transporte.")

            elif option == 5:
                print(f"\nQ5: Consulta de la validez de un camino.")

            elif option == 6:
                print(f"\nQ6: Consulta de las rutas alcanzables por una determinada cantidad de saltos dentro del grafo.")
                
            elif option == 7:
                print(f"\nQ7: Consulta de rutas alternativas con un transbordo.")

            elif option == 8:
                print(f"\nQ8: Consulta de todas las estaciones relacionadas a una línea.")

            else:
                print("Invalid option. Please try again.")
        except Exception as e:
            log.error("Error en consulta Dgraph (opcion %s): %s", option, e)
            print(f"Error al ejecutar la consulta: {e}")


def main():
    try:
        cass_session = connect_cassandra()
        db_session = connect_mongo()
        dgraph_client, dgraph_stub = connect_dgraph()        
    except Exception:
        log.error("No se pudo iniciar. Revisa que las 3 bases se esten ejecutando")
        return
    
    while(True):
        print_main_menu();
        try:
            opcion = int(input("\nEnter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        
        if opcion == 5:
            print("Exiting logistics application...")
            break
            
        if opcion == 1: #poblar
            break
        if opcion == 2 : ##MONGO
            actions_mongo(db_session)
            break
        if opcion == 3: ## DGRAPH
            actions_dgraph(dgraph_client)
            break

        if opcion == 4: ##Cassandra
            actions_cassandra(cass_session);
            break

             
                    

if __name__ == "__main__":
    main()