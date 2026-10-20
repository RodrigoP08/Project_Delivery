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
docker run --name logistics -p 9042:9042 -d cassandra

# Si ya existe el contenedor, solo iniciarlo
docker start logistics
```
### Iniciar MongoDB
```
docker run --name mongodb -d -p 27017:27017 mongo
# Si ya existe el contenedor, solo iniciarlo
docker start mongodb
```

### Inicializar Dgraph
ESTO TODAVIA NO SE BIEN
```
docker run --name dgraph -d -p 8080:8080 -p 9080:9080 dgraph/standalone:latest
# Si ya existe el contenedor, solo iniciarlo
docker start dgraph
```
API services
```
python -m uvicorn main:app --reload
```

Una vez que todo este ejecutandose, se tienen que poblar las bases de datos
```
python populate.py
```

