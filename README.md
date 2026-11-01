# Project_Delivery
- Rodrigo Peña Muñoz		      757454<br>
- Cynthia Gabriela González Rayas     	757775<br>
- Sofia Marcela Jiménez López 		758568<br>


## Requisitos previos

- Python 3.8 o superior
- Docker

## 1. Configurar el entorno

### Instalar dependencias de Python

```bash
# Crear y activar entorno virtual (recomendado)

# Linux / Mac:
python3 -m venv venv
source venv/bin/activate

# Windows:
python3 -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar dependencias del proyecto
pip install -r requirements.txt
```

### Iniciar Cassandra

```bash
# Crear y arrancar el contenedor (primera vez)
docker run --name transport_Cassandra -p 9042:9042 -d cassandra
# Si ya existe el contenedor, solo iniciarlo
docker start transport_Cassandra
```
### Iniciar MongoDB
```
# Crear y arrancar el contenedor (primera vez)
docker run --name transporte_mongodb -d -p 27017:27017 mongo
# Si ya existe el contenedor, solo iniciarlo
docker start transporte_mongodb
```

### Inicializar Dgraph
```
# Crear y arrancar el contenedor (primera vez)
docker run --name transporte_dgraph -d -p 8080:8080 -p 9080:9080 dgraph/standalone:latest
# Si ya existe el contenedor, solo iniciarlo
docker start transporte_dgraph
```
## 2. Ejecutar aplicacion
```
python main.py
```

