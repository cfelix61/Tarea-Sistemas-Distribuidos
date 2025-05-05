from Esclavo.interfaz_log import Logger
import Pyro5.api

def main():
    daemon = Pyro5.api.Daemon()
    ns = Pyro5.api.locate_ns()  # Localiza el nameserver

    uri = daemon.register(Logger())
    ns.register("log_centralizado", uri)  # Registra el objeto con nombre lógico

    print("Servidor RMI registrado en el NameServer como 'log_centralizado'")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
