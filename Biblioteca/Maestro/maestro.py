import requests
import time
import sys
import os
sys.path.append(os.path.abspath(".."))

from log_client import enviar_log

# Esclavos mapeados por tipo de documento
ESCLAVOS = {
    "libro": "http://localhost:5001/query",
    "tesis": "http://localhost:5002/query",
    "articulo": "http://localhost:5003/query",
    "video": "http://localhost:5004/query"
}

def buscar(query, tipo_doc, edad):
    t_ini = time.time()
    resultados = []

    # Buscar por título, broadcast a todos los esclavos
    if query:
        for url in ESCLAVOS.values():
            try:
                # Cambié a POST en lugar de GET
                r = requests.post(url, json={"query": query, "edad": edad})  # Cambié a POST
                if r.ok:
                    resultados += r.json()
            except Exception as e:
                print("Error con esclavo:", e)

    # Buscar por tipo de docu, multicast a los esclavos por siaca manolo
    elif tipo_doc:
        tipos = tipo_doc.split("+")
        for tipo in tipos:
            url = ESCLAVOS.get(tipo)
            if url:
                try:
                    r = requests.post(url, json={"query": "", "edad": edad})  # Cambié a POST
                    if r.ok:
                        resultados += r.json()
                except Exception as e:
                    print(f"Error con el esclavo de tipo {tipo}:", e)

    # Ordenar por puntaje 
    resultados.sort(key=lambda x: x.get("score", 0), reverse=True)

    # Log de la operación
    t_fin = time.time()
    enviar_log({ # invoco la funcion que envia los datos al servidor RMI de log
        "inicio": t_ini,
        "fin": t_fin,
        "maquina": "maestro",
        "tipo": "maestro",
        "query": query,
        "tiempo_total": round(t_fin - t_ini, 4),
        "score": len(resultados),
        "edad": edad,
        "rango": get_rango_etario(edad)
    })

    return resultados

def get_rango_etario(edad):
    if edad < 16:
        return "menor de 16"
    elif edad <= 25:
        return "16-25"
    elif edad <= 40:
        return "26-40"
    else:
        return "mayor de 40"

if __name__ == "__main__":
    while True:
        query = input("Ingrese búsqueda (Vacío para buscar por tipo): ")
        tipo_doc = input("Ingrese tipo de documento (o deje vacío para buscar por título): ")
        edad = int(input("Edad del usuario: "))
        r = buscar(query, tipo_doc, edad)
        print(f"Resultados ({len(r)}):")
        for i in r:
            print("-", i["titulo"])
