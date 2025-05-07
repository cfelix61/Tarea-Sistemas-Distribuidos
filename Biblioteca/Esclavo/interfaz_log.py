import Pyro5.api

@Pyro5.api.expose #permite que llamen a los metodos
class Logger:
    def __init__(self):
        self.logs = [] #inicializo la lista de logs vacíos

    def log(self, data: dict): #este es el método que llama log_client al hacer log_server.log(data)
        print("[LOG RMI] Entrada recibida:", data)
        self.logs.append(data)
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(str(data) + "\n")

    def get_logs(self):
        return self.logs #para consultar la lista de logs guardados
