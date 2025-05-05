from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

# Distribución de esclavos por tipo de documento
ESCLAVOS = {
    "libro": "http://localhost:5001",
    "tesis": "http://localhost:5002",
    "video": "http://localhost:5003",
    "articulo": "http://localhost:5004"
}

# Preferencias por rango etario
PREFERENCIAS = {
    "10-15": "ciencia ficcion",
    "16-25": "tecnologia",
    "26-99": "investigacion"
}

@app.route("/query")
def query():
    titulo = request.args.get("titulo")
    tipo_doc = request.args.get("tipo_doc")
    edad = int(request.args.get("edad", 18))
    rango = "10-15" if edad <= 15 else "16-25" if edad <= 25 else "26-99"
    preferencia = PREFERENCIAS[rango]

    start_time = time.time()

    if titulo:
        resultados = []
        for url in ESCLAVOS.values():
            r = requests.get(f"{url}/buscar", params={"titulo": titulo, "edad": edad})
            resultados.extend(r.json())
    elif tipo_doc:
        resultados = []
        tipos = tipo_doc.split("+")
        for tipo in tipos:
            url = ESCLAVOS.get(tipo)
            if url:
                r = requests.get(f"{url}/buscar", params={"titulo": titulo or "", "edad": edad})
                resultados.extend(r.json())
    else:
        return jsonify({"error": "Debe indicar un titulo o tipo_doc"}), 400

    resultados.sort(key=lambda x: -x['ranking'])

    # Log RMI client (simplificado)
    import Pyro5.api
    with Pyro5.api.Proxy("PYRO:logger@localhost:9090") as remote_logger:
        remote_logger.log({
            "inicio": start_time,
            "fin": time.time(),
            "maquina": "localhost",
            "tipo": "maestro",
            "query": request.query_string.decode(),
            "score": resultados[0]['ranking'] if resultados else 0,
            "edad": edad
        })

    return jsonify(resultados)

if __name__ == "__main__":
    app.run(port=5000)
