from flask import Flask, request, jsonify
import json
import time
import sys

TIPO = sys.argv[1] if len(sys.argv) > 1 else "libro"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5001
FILE = f"data/{TIPO}s.json"

app = Flask(__name__)

PREFERENCIAS = {
    "10-15": "ciencia ficcion",
    "16-25": "tecnologia",
    "26-99": "investigacion"
}

def calcular_ranking(titulo, documento, preferencia):
    score = 0
    for termino in titulo.lower().split():
        if termino in documento['titulo'].lower():
            score += 1
    if preferencia.lower() in documento['genero'].lower():
        score += 2
    return score

@app.route("/buscar")
def buscar():
    titulo = request.args.get("titulo", "")
    edad = int(request.args.get("edad", 18))
    rango = "10-15" if edad <= 15 else "16-25" if edad <= 25 else "26-99"
    preferencia = PREFERENCIAS[rango]

    start_time = time.time()
    with open(FILE, encoding="utf-8") as f:
        data = json.load(f)

    resultados = []
    for doc in data:
        rank = calcular_ranking(titulo, doc, preferencia)
        if rank > 0:
            doc['ranking'] = rank
            resultados.append(doc)

    # Log RMI client (simplificado)
    import Pyro5.api
    with Pyro5.api.Proxy("PYRO:logger@localhost:9090") as remote_logger:
        remote_logger.log({
            "inicio": start_time,
            "fin": time.time(),
            "maquina": f"localhost:{PORT}",
            "tipo": "esclavo",
            "query": titulo,
            "score": max([d['ranking'] for d in resultados], default=0),
            "edad": edad
        })

    return jsonify(resultados)

if __name__ == "__main__":
    app.run(port=PORT)

# rmi_logger_server.py
import Pyro5.api
from datetime import datetime

@Pyro5.api.expose
class Logger:
    def __init__(self):
        self.logs = []

    def log(self, entry):
        entry["timestamp"] = datetime.now().isoformat()
        print("LOG:", entry)
        self.logs.append(entry)


daemon = Pyro5.server.Daemon(port=9090)
uri = daemon.register(Logger, "logger")
print("Logger RMI server listo en:", uri)
daemon.requestLoop()
