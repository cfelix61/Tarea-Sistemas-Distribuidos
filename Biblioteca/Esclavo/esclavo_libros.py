from flask import Flask, request, jsonify
import json
import time
import sys
import os
sys.path.append(os.path.abspath(".."))

from log_client import enviar_log

app = Flask(__name__)
PORT = 5001  

@app.route('/query', methods=['POST'])
def buscar():
    datos = request.json
    query = datos['query']
    edad = datos.get('edad', 20)

    t_ini = time.time()

    with open("data/libros.json") as f:
        libros = json.load(f)

    resultados = [l for l in libros if query.lower() in l['titulo'].lower()]
    score = len(resultados)
    t_fin = time.time()

    enviar_log({#invoco la weaita de func que envia los datos al servidor RMI de log
        "inicio": t_ini,
        "fin": t_fin,
        "maquina": f"esclavo:{PORT}",
        "tipo": "esclavo",
        "query": query,
        "tiempo_total": round(t_fin - t_ini, 4),
        "score": score,
        "edad": edad,
        "rango": get_rango_etario(edad)
    })

    return jsonify(resultados)

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
    app.run(port=5001)
