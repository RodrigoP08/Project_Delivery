
from connect import setup_logging, connect_cassandra, connect_mongo, connect_dgraph,log, sys

from Cassandra import cassandra_menus
from Mongo import mongo_menus
from Dgraph import dgraph_menus

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
            mongo_menus.actions_mongo(db_session)
            break
        if opcion == 3: ## DGRAPH
            dgraph_menus.actions_dgraph(dgraph_client)
            break

        if opcion == 4: ##Cassandra
            cassandra_menus.actions_cassandra(cass_session);
            break

             
                    

if __name__ == "__main__":
    main()