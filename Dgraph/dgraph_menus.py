import os
import sys

# Obtiene la ruta de la carpeta actual y sube un nivel hacia la raíz del proyecto
ruta_raiz = os.path.abspath( os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ruta_raiz)
from connect import log 

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
