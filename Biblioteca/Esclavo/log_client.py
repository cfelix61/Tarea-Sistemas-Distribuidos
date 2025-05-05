import Pyro5.api

def enviar_log(data):
    try:
        log_server = Pyro5.api.Proxy("PYRONAME:log_centralizado")
        log_server.log(data)
    except Exception as e:
        print("Error al enviar log RMI:", e)
