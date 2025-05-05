import Pyro5.api

@Pyro5.api.expose
class ServicioChat:
    def __init__(self):
        self.clientes = []

    def alta(self, cliente_uri, apodo):
        print("Cliente conectado:", cliente_uri)
        cliente_proxy = Pyro5.api.Proxy(cliente_uri)  # Crear un proxy para el cliente
        self.clientes.append(cliente_proxy)
        print(f"CLIENTES: {len(self.clientes)} conectados")
        # Notificar a todos los clientes sobre el nuevo cliente de la sala de chat
        for c in self.clientes:
            if str(c._pyroUri) != str(cliente_uri):
                try:
                    # Crear un nuevo proxy en el hilo actual
                    with Pyro5.api.Proxy(c._pyroUri) as cliente_proxy:
                        cliente_proxy.entrada(apodo)  # Llamar al método remoto
                except Exception as e:
                    #print(f"Error enviando a {c._pyroUri}: {e}")
                    pass

    def baja(self, cliente_uri, apodo):
        self.clientes = [c for c in self.clientes if c._pyroUri != cliente_uri]
        print(f"Cliente desconectado: {apodo} | {len(self.clientes)} clientes restantes")
        for c in self.clientes:
            if str(c._pyroUri) != str(cliente_uri):
                try:
                    # Crear un nuevo proxy en el hilo actual
                    with Pyro5.api.Proxy(c._pyroUri) as cliente_proxy:
                        cliente_proxy.salida(apodo)  # Llamar al método remoto
                except Exception as e:
                    #print(f"Error enviando a {c._pyroUri}: {e}")
                    pass


    def envio(self, esc_uri, apodo, mensaje):
        #print(f"{apodo} dice > {mensaje}")
        for c in self.clientes:
            if str(c._pyroUri) != str(esc_uri):  # Evitar reenvío al remitente
                try:
                    # Crear un nuevo proxy en el hilo actual
                    with Pyro5.api.Proxy(c._pyroUri) as cliente_proxy:
                        cliente_proxy._pyroTimeout = 8  # Establecer tiempo límite de 5 segundos
                        print(f"Enviando a {cliente_proxy._pyroUri}")
                        cliente_proxy.notificacion(apodo, mensaje)  # Llamar al método remoto
                except Pyro5.errors.TimeoutError:
                    print(f"Tiempo de espera agotado para {c._pyroUri}")
                except Exception as e:
                    print(f"Error enviando a {c._pyroUri}: {e}")