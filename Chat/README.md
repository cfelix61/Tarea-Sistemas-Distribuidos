# Servicio RMI de Sala de Chat
Este servicio permite crear una sala de chat, enviar mensajes y recibir mensajes de otros usuarios en la sala.

## Requisitos
- Python 3.8 o superior
- Pyro5 `pip install Pyro5`

## Explicación
* `client/main.py`: Contiene una llamada al servicio de chat donde se entrega una URI del cliente permitiendo al servidor redirigir mensajes a la terminal del cliente.

    Funciones expuestas por el cliente (`client/cliente.py`):

    * **Notificacion:** Entrega el mensaje al cliente en terminal.
    * **Entrada:** Entrega información de nuevos usuarios conectados a la sala de chat.
    * **Salida:** Entrega información de usuarios desconectados de la sala de chat.

* `server/main.py`: Contiene la implementación del servicio de chat, indicando su configuracion inicial y registro en el servidor de nombres de Pyro5.

    Funciones expuestas por el servidor (`server/servicioChat.py`):

    * **Alta:** Permite a un cliente unirse a la sala de chat, ingresandolo en un arreglo de clientes y notificando a los demas clientes de su ingreso.

    * **Baja:** Formaliza la desconexión de un cliente, eliminandolo del arreglo de clientes y notificando a los demas clientes de su salida.

    * **Envio:** Permite enviar mensajes a todos los clientes conectados a la sala de chat, notificiando a cada cliente el apodo de quien envió el mensaje y el mensaje en sí.

## Ejecución

1. Iniciar el servidor de nombres de Pyro5:
```bash
python -m Pyro5.nameserver -n 127.0.0.1 -p 4002
```

2. Iniciar el servidor de la sala de chat en una terminal nueva (carpeta `server`):

```bash
python servidor.py
```

3. Iniciar el cliente de la sala de chat en otra terminal nueva (carpeta `client`):

```bash
python main.py <apodo>
```

4. Iniciar el cliente de la sala de chat en otra terminal nueva (carpeta `client`):

```bash
python main.py <apodo2>
```