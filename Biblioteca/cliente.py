import requests

def solicitar_datos():
    query = input("Ingrese búsqueda (Vacío para buscar por tipo): ").strip()
    tipo_doc = input("Ingrese tipo de documento (o deje vacío para buscar por título): ").strip()

    if not query and not tipo_doc:
        print("Se entregarán todos los documentos.")
        tipo_doc = "libros+tesis+articulos+videos"

    entrada = input("Entregue su edad (por defecto 0): ").strip()
    edad = int(entrada) if entrada.isdigit() else 0

    while edad <= 0 or edad > 120:
        print("Edad no válida. Ingrese nuevamente.")
        entrada = input("Entregue su edad (por defecto 0): ").strip()
        edad = int(entrada) if entrada.isdigit() else 0

    return {
        "query": query,
        "tipo_doc": tipo_doc,
        "edad": edad
    }

def mostrar_resultados(resultados, query=""):
    if query:
        titulos = [doc["titulo"].lower() for doc in resultados]
        if query.lower() not in titulos:
            print("\nNo se encontró una coincidencia exacta.")
            print("Aquí hay algunas recomendaciones similares:\n")
    print(f"\nResultados ({len(resultados)}):")
    for i in resultados:
        print(f"- {i['titulo']} (Score: {i['score']})")
    print("\n" + "-"*50 + "\n")

def main():
    print("Cliente de búsqueda iniciado. Presiona Ctrl+C para salir.\n")
    while True:
        try:
            datos = solicitar_datos()
            response = requests.post("http://localhost:5000/buscar", json=datos)

            if response.ok:
                resultados = response.json()
                mostrar_resultados(resultados, datos["query"])
            else:
                print("Error:", response.text)

        except KeyboardInterrupt:
            print("\nSaliendo del cliente...")
            break
        except Exception as e:
            print("Error al conectar con el servidor maestro:", e)

if __name__ == "__main__":
    main()
