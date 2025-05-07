import Pyro5.api

def enviar_log(data):
    try:
        log_server = Pyro5.api.Proxy("PYRONAME:log_centralizado") #conectamos al servidor RMI por el nombre que defini
        log_server.log(data) # Le envío los datos
    except Exception as e:
        print("Error al enviar log RMI:", e)
