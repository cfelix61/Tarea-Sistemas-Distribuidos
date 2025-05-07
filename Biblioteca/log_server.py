from Esclavo.interfaz_log import Logger
import Pyro5.api

def main():
    daemon = Pyro5.api.Daemon() # creo el server
    ns = Pyro5.api.locate_ns()  # Localiza el nameserver

    uri = daemon.register(Logger()) #Expone el logger como RMI xd
    ns.register("log_centralizado", uri)  # Lo registra en el name server con el nombre 'log_centralizado'

    print("Servidor RMI registrado en el NameServer como 'log_centralizado'")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
