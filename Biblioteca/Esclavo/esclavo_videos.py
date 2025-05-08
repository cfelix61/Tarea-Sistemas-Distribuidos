from flask import Flask, request, jsonify
import json
import time
import sys
import os
import unicodedata
sys.path.append(os.path.abspath(".."))

from log_client import enviar_log

app = Flask(__name__)
PORT = 5004

def normalizar(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto.lower().strip())
        if unicodedata.category(c) != 'Mn'
    )

def get_rango_etario(edad):
    if edad < 16:
        return "menor de 16"
    elif edad <= 25:
        return "16-25"
    elif edad <= 40:
        return "26-40"
    else:
        return "mayor de 40"

def calcular_relevancia_titulo(titulo, query):
    titulo_tokens = titulo.lower().split()
    query_tokens = query.lower().split()
    return sum(1 for q in query_tokens if q in titulo_tokens)

def calcular_score(articulo, query, rango_etario):
    # Calcular puntaje base por relevancia de título si hay un query
    base_score = calcular_relevancia_titulo(articulo["titulo"], query)
    genero = articulo.get("genero", "").strip().lower()

    # Bonus por coincidencia exacta con el título
    if normalizar(articulo["titulo"]) == normalizar(query):
        base_score += 1  # Bonus por match exacto

    # Bonus por rango etario y género
    if rango_etario == "menor de 16":
        if genero in ["sci-fi", "educacion"]:
            base_score += 2
    elif rango_etario == "16-25":
        if genero in ["tecnolgia", "ciencia", "educacion", "emprendimiento"]:
            base_score += 2
    elif rango_etario == "26-40":
        if genero in ["historia", "politica"]:
            base_score += 2
    elif rango_etario == "mayor de 40":
        if genero in ["biografia", "arte"]:
            base_score += 2

    return base_score




@app.route('/query', methods=['POST'])
def buscar():
    datos = request.json
    query = datos['query']
    edad = datos.get('edad', 20)
    rango = get_rango_etario(edad)

    t_ini = time.time()

    with open("data/videos.json") as f:
        articulos = json.load(f)

    resultados = []

    if query.strip() == "":
        for articulo in articulos:
            score = calcular_score(articulo, "", rango)
            resultado = articulo.copy()
            resultado["score"] = score
            resultados.append(resultado)
    else:
        for articulo in articulos:
            score = calcular_score(articulo, query, rango)
            if score > 0:
                resultado = articulo.copy()
                resultado['score'] = score
                resultados.append(resultado)

    resultados.sort(key=lambda a: a['score'], reverse=True)
    score_total = sum(r['score'] for r in resultados)

    t_fin = time.time()

    enviar_log({
        "inicio": t_ini,
        "fin": t_fin,
        "maquina": f"esclavo:{PORT}",
        "tipo": "esclavo",
        "query": query,
        "tiempo_total": round(t_fin - t_ini, 4),
        "score": score_total,
        "edad": edad,
        "rango": rango
    })

    return jsonify(resultados)

if __name__ == "__main__":
    app.run(port=PORT)
