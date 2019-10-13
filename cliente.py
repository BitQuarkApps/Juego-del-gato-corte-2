import websocket
import time
import json
try:
    import thread
except ImportError:
    import _thread as thread

from agente.agente import AgenteJugador

my_id = None
agente = None

def on_message(ws, message):
    global agente
    global my_id
    message = json.loads(message)
    print(message)
    
    # Si el message tiene un id significa que todavia no ha iniciado el juego
    if "id" in message:
        if message["id"] == -1:
            print("ya no hay cupo")
            ws.close()
        else:
            print("mi id es: " + str(message["id"]))
            my_id =  message["id"]
            agente = AgenteJugador(my_id)

    # Si no tiene id siginifica que el juego ya inicio
    else:
        if "ganador" in message:
            print(f"El ganador es : {message['ganador']}")
            ws.close()
        else:
            turno = message["turno"]
            matriz = message["matriz"]
            ganador = agente.puede_ganar(matriz, my_id)
            agente.update_tablero(matriz)
            print("\n")
            for row in matriz:
                print(f"[ {row} ]")
            print("\n")
            # proceso de acuerdo a mis reglas
            minimax, x, y = agente.minimax()
            if minimax != None and x != None and y != None:
                print(f'Minimax => {minimax}, x => {x}, y => {y}')
                # envio mi posicion de tiro
                my_message = json.dumps({"x": x, "y": y, "ganador": ganador, "id": my_id})
                ws.send(my_message)
            
def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        print("Conectado...")
    thread.start_new_thread(run, ())

websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://localhost:9000",
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)
ws.on_open = on_open
ws.run_forever()
