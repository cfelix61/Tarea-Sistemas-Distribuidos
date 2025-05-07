# Tarea-Sistemas-Distribuidos
"""
biblioteca/
├── esclavo/
│   ├── esclavo_libros.py         # HTTP server
│   ├── interfaz_log.py           # Interfaz Pyro5
│   ├── log_client.py
|    data/
│       ├── libros_esclavo1.json
│       ├── libros_esclavo2.json             # Cliente RMI que envía logs
├── maestro/
│   ├── maestro.py                # Consulta a esclavos
│   ├── log_client.py             # Cliente RMI desde maestro
|
|── log_server.py             # Servidor RMI centralizado
├── README.md   


# Biblioteca Digital Distribuida

## Lenguaje y Framework
- Python 3.10
- Flask
- Pyro5

## Estructura
- `maestro/`: dirige las consultas y enruta según tipo de documento.
- `esclavo/`: contiene 4 codigos como microservicios para libros, tesis, artículos y videos.
- `data/`: base de datos para los esclavos, en formato JSON.

## Puertos de los esclavos:
-   http://localhost:5001/query para esclavo_libros.py

-   http://localhost:5002/query para esclavo_tesis.py

-   http://localhost:5003/query para esclavo_articulos.py

-   http://localhost:5004/query para esclavo_videos.py

## Instalar dependencias
-   pip install flask requests
-   pip install Pyro5

## Ejecución en bash:
1. Ejecutar los esclavos (cada uno en una terminal diferente y desde la carpeta Biblioteca):
python esclavo/esclavo_libros.py
python esclavo/esclavo_tesis.py
python esclavo/esclavo_articulos.py
python esclavo/esclavo_videos.py

2. Ejecutar el maestro:
-   python maestro/maestro.py

## Ejecución en powershell:
1. Iniciar el Name Server en Powershell:
-   python -m Pyro5.nameserver

2. Ejecutar el server de los logs en la carpeta Biblioteca
- python log_server.py

3. Ejecutar los esclavos (cada uno en una terminal diferente y desde la carpeta Esclavo):
python esclavo_libros.py
python esclavo_tesis.py
python esclavo_articulos.py
python esclavo_videos.py


4. Ejecutar el maestro (terminal distinta y carpeta Maestro):
-   python maestro.py

5. Ejecutar log_viewer en distinta terminal, es de ejecución única, no queda esperando respuesta. Actualiza el .txt que guarda los Logs.
-   python log_viewer.py
## Consultas 
- Buscar por título:
    Ingrese búsqueda: Historia de la Tierra
    Ingrese tipo de documento (o deje vacío para buscar por título):
    Edad del usuario: 16
- Buscar por tipo:
    Ingrese búsqueda:
    Ingrese tipo de documento (o deje vacío para buscar por título): libro+tesis
    Edad del usuario: 25
"""

