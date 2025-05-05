import Pyro5.api

@Pyro5.api.expose
class Cliente:
    def notificacion(self, apodo, mensaje):
        print(f"\n{apodo} dice > {mensaje}")
        
        #print("\nEscriba su mensaje: ", end="", flush=True)  

    def entrada(self, apodo):
        print(f"\n{apodo} ha ingresado al chat.")
        #print("\nEscriba su mensaje: ", end="", flush=True)  

    def salida(self, apodo):
        print(f"\n{apodo} ha salido del chat.")
        #print("\nEscriba su mensaje: ", end="", flush=True)  