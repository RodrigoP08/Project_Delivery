import os
import sys

# Obtiene la ruta de la carpeta actual y sube un nivel hacia la raíz del proyecto
ruta_raiz = os.path.abspath( os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ruta_raiz)
from connect import log 

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
            try:
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
            except Exception as e:
                log.error("Error en consulta CASSANDRA (opcion %s): %s", option, e)
                print(f"Error al ejecutar la consulta: {e}")
                