import sys
import threading
import Pyro5.api
from cliente import Cliente

SERVER_HOST = "127.0.0.1"
NS_PORT = 4002
SALIR = "EXIT"

# Función principal del cliente
def main():
    if len(sys.argv) != 2:
        print("Uso: python cliente_chat.py <apodo>")
        sys.exit(1)

    apodo = sys.argv[1]

    # Crear objeto cliente y registrar en daemon
    cliente = Cliente()
    daemon = Pyro5.api.Daemon()
    uri_cliente = daemon.register(cliente)

    # Buscar el servicio de chat
    ns = Pyro5.api.locate_ns(host=SERVER_HOST, port=NS_PORT)
    chat = Pyro5.api.Proxy(ns.lookup("Chat"))

    # Alta en el chat
    chat.alta(uri_cliente, apodo)

    # Lanzar hilo para escuchar notificaciones (mantener daemon activo)
    def loop_notificaciones():
      
        daemon.requestLoop()

    threading.Thread(target=loop_notificaciones, daemon=True).start()

    try:
        print(f"{apodo} dice > ", end="", flush=True)
        while True:
            msg = input()
            if msg.strip().upper() == SALIR:
                print("Saliendo del chat...")
                chat.baja(uri_cliente, apodo)  # Pasar uri_cliente
                break
            else:
                chat.envio(uri_cliente, apodo, msg)  # Pasar uri_cliente
                print(f"{apodo} dice > ", end="", flush=True)
    except KeyboardInterrupt:
        chat.baja(uri_cliente, apodo)  # Pasar uri_cliente
        print("\nSaliste del chat.")

if __name__ == "__main__":
    main()
