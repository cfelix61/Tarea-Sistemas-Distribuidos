import requests
import time
import sys
import os
sys.path.append(os.path.abspath(".."))

from log_client import enviar_log

# Esclavos mapeados por tipo de documento
ESCLAVOS = {
    "libros": "http://localhost:5001/query",
    "tesis": "http://localhost:5002/query",
    "articulos": "http://localhost:5003/query",
    "videos": "http://localhost:5004/query"
}

def get_rango_etario(edad):
    if edad < 16:
        return "menor de 16"
    elif edad <= 25:
        return "16-25"
    elif edad <= 40:
        return "26-40"
    else:
        return "mayor de 40"

def buscar(query, tipo_doc, edad):
    t_ini = time.time()
    resultados = []
    rango_etario = get_rango_etario(edad)

    # Buscar por título, broadcast a todos los esclavos
    if query:
        for url in ESCLAVOS.values():
            try:
                r = requests.post(url, json={"query": query, "edad": edad})  # Cambié a POST
                if r.ok:
                    resultados += r.json()
            except Exception as e:
                print("Error con esclavo:", e)

    # Buscar por tipo de documento, multicast a los esclavos
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

    # Si no se encontraron resultados, mostrar mensaje
    if not resultados:
        print("No se encontraron resultados.")
    
    # Ordenar por puntaje
    resultados.sort(key=lambda x: x.get("score", 0), reverse=True)

    # Log de la operación
    t_fin = time.time()
    enviar_log({  # invoco la funcion que envia los datos al servidor RMI de log
        "inicio": t_ini,
        "fin": t_fin,
        "maquina": "maestro",
        "tipo": "maestro",
        "query": query,
        "tiempo_total": round(t_fin - t_ini, 4),
        "score": len(resultados),
        "edad": edad,
        "rango": rango_etario
    })

    return resultados

if __name__ == "__main__":
    while True:
        query = input("Ingrese búsqueda (Vacío para buscar por tipo): ")
        tipo_doc = input("Ingrese tipo de documento (o deje vacío para buscar por título): ")

        if query == "" and tipo_doc == "":
            print("Se entregaran todos los documentos.")
            tipo_doc = "libros+tesis+articulos+videos"

        entrada = input("Entregue su edad (por defecto 0): ").strip()

        edad = int(entrada) if entrada.isdigit() else 0

        while (edad <= 0 or edad > 120 or edad == ""):
            print("Edad no válida. Ingrese nuevamente.")
            entrada = input("Entregue su edad (por defecto 0): ").strip()
            edad = int(entrada) if entrada.isdigit() else 0

        r = buscar(query, tipo_doc, edad)
        print(f"Resultados ({len(r)}):")
        for i in r:
            print(f"- {i['titulo']} (Score: {i['score']})")
