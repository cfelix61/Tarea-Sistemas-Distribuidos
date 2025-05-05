import Pyro5.api

@Pyro5.api.expose
class Logger:
    def __init__(self):
        self.logs = []

    def log(self, data: dict):
        print("[LOG RMI] Entrada recibida:", data)
        self.logs.append(data)

    def get_logs(self):
        return self.logs
