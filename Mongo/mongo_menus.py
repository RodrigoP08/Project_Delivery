import os
import sys

# Obtiene la ruta de la carpeta actual y sube un nivel hacia la raíz del proyecto
ruta_raiz = os.path.abspath( os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ruta_raiz)
from connect import log 

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
