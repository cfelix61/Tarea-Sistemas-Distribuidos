from flask import Flask, request, jsonify
import requests
import time
import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.abspath(".."))

from log_client import enviar_log

app = Flask(__name__)
PORT = 5000

load_dotenv()  # Cargar las variables del archivo .env

ESCLAVOS = {
    "libros": os.getenv("ESCLAVO_LIBROS"),
    "tesis": os.getenv("ESCLAVO_TESIS"),
    "articulos": os.getenv("ESCLAVO_ARTICULOS"),
    "videos": os.getenv("ESCLAVO_VIDEOS")
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

def distribuir_busqueda(query, tipo_doc, edad):
    t_ini = time.time()
    resultados = []
    rango_etario = get_rango_etario(edad)

    if query and not tipo_doc:
        for url in ESCLAVOS.values():
            try:
                r = requests.post(url, json={"query": query, "edad": edad})
                if r.ok:
                    resultados += r.json()
            except Exception as e:
                print("Error con esclavo:", e)

    elif tipo_doc and not query:
        tipos = tipo_doc.split("+")
        for tipo in tipos:
            url = ESCLAVOS.get(tipo)
            if url:
                try:
                    r = requests.post(url, json={"query": "", "edad": edad})
                    if r.ok:
                        resultados += r.json()
                except Exception as e:
                    print(f"Error con el esclavo de tipo {tipo}:", e)

    elif tipo_doc and query != "":
        tipos = tipo_doc.split("+")
        for tipo in tipos:
            url = ESCLAVOS.get(tipo)
            if url:
                try:
                    r = requests.post(url, json={"query": query, "edad": edad})
                    if r.ok:
                        resultados += r.json()
                except Exception as e:
                    print(f"Error con el esclavo de tipo {tipo}:", e)
    resultados.sort(key=lambda x: x.get("score", 0), reverse=True)

    t_fin = time.time()
    enviar_log({
        "inicio": t_ini,
        "fin": t_fin,
        "maquina": f"maestro:{PORT}",
        "tipo": "maestro",
        "query": query + " " + tipo_doc,
        "tiempo_total": round(t_fin - t_ini, 4),
        "score": len(resultados),
        "edad": edad,
        "rango": rango_etario
    })

    return resultados

@app.route("/buscar", methods=["POST"])
def buscar():
    data = request.json
    query = data.get("query", "").strip()
    tipo_doc = data.get("tipo_doc", "").strip()
    edad = data.get("edad", 0)

    if not query and not tipo_doc:
        tipo_doc = "libros+tesis+articulos+videos"

    try:
        edad = int(edad)
        if edad <= 0 or edad > 120:
            return jsonify({"error": "Edad no válida"}), 400
    except:
        return jsonify({"error": "Edad no válida"}), 400

    resultados = distribuir_busqueda(query, tipo_doc, edad)
    return jsonify(resultados)

if __name__ == "__main__":
    app.run(port=PORT)
