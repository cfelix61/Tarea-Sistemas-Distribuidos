import Pyro5.api

def ver_logs():
    try:
        # Conectarse al objeto remoto con nombre 'log_centralizado'
        log_server = Pyro5.api.Proxy("PYRONAME:log_centralizado")
        logs = log_server.get_logs()
        print(f"\nSe encontraron {len(logs)} logs:\n")
        for i, log in enumerate(logs, 1):
            print(f"{i}. {log}")
    except Exception as e:
        print("Error al recuperar logs:", e)

if __name__ == "__main__":
    ver_logs()
