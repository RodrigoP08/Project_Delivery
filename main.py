
from connect import setup_logging, connect_cassandra, log, sys

from Cassandra import model



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
        0: "",
        1: "",
        2: "",
        3: "",
        4: "",
        5: "",
        6: "",
        7: "",
        8: "",
        9: "EXIT",
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
                print(f"\nQ1: ")
    
            elif option == 1:
                print(f"\nQ1: ")
                # model.function_example(session)
    
            elif option == 2:
                print(f"\nQ2: ")
    
            elif option == 3:
                print(f"\nQ3:")
    
            elif option == 4:
                print(f"\nQ4:")
    
            elif option == 5:
                print(f"\nQ5:")
    
            elif option == 6:
                print(f"\nQ6:")
    
            elif option == 7:
                print(f"\nQ7:")
                    
            elif option == 8:
                print(f"\nQ8")
            elif option == 9:
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")
        
def main():
    try:
        cass_session = connect_cassandra()
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
        
        if opcion == "5":
            print("Exiting logistics application...")
            sys.exit(0)
            break
        if opcion == 1: #poblar
            break
        if opcion == 2 : ##MONGO
            break
        if opcion == 3: ## DGRAPH
            break
        if opcion == 4: ##Cassandra
            actions_cassandra(cass_session);                
            break
                    

if __name__ == "__main__":
    main()