from tornado import websocket
import tornado.ioloop
import json
import time

# PATRON DE DISEÑO SINGLETON PARA QUE SOLO HAYA UNA INSTANCIA DE ESTA CLASE
class Game(object):

    class __Game:
        def __init__(self):
            self.clients = 0
            self.matriz = [[None for _ in range(3)] for _ in range(3)]
            self.bandera_turno = False
            self.clients_arr = []

        def __str__(self):
            return self.clients

    instance = None

    def __new__(cls):
        if not Game.instance:
            Game.instance = Game.__Game()
        return Game.instance
        

# SE CREA UNA INSTANCIA DE ESTA CLASE POR CADA CONEXIÓN
class EchoWebSocket(websocket.WebSocketHandler):
    
    # Se ejecuta cuando se conecta un cliente
    def open(self):
        self.game = Game()
        self.game.clients_arr.append(self)
        
        # Si hay cupo le envia su id
        if self.game.clients == 0:
            self.write_message(json.dumps({ "id": self.game.clients }))
            print ("Websocket con id " + str(self.game.clients) + " conectado")
            self.game.clients += 1
        
        # Si se conecta el ultimo cliente iniciar el juego
        elif self.game.clients == 1:
            self.write_message(json.dumps({ "id": self.game.clients }))
            print ("Websocket con id " + str(self.game.clients) + "conectado")
            self.game.clients += 1

            # Envia el mensaje que al cliente que tira primero
            self.game.bandera_turno = not self.game.bandera_turno # cambio de turno para el siguiente tiro
            message = json.dumps({ "turno": 0, "matriz": self.game.matriz })
            print("turno: 0")
            time.sleep(2)
            self.game.clients_arr[0].write_message(message)

        # Si ya no hay cupo manda un id de -1
        else:
            print ("Websocket sin cuppo")
            self.write_message(json.dumps({"id": -1 }))

    # Se ejecuta cuando recibe un mensaje del ultimo cliente que tiro        
    def on_message(self, message):
        print(f"Mensaje => {message}")

        message = json.loads(message)
        
        x = message["x"]
        y = message["y"]
        cliente_id = message["id"]
        ganador = message["ganador"]

        if ganador:
            print("Gané el juego, mi id es: " + str(cliente_id))
            message = json.dumps({ "ganador": cliente_id })
            self.game.clients_arr[0].write_message(message)
            self.game.clients_arr[1].write_message(message)
            print("\n")
            for row in self.game.matriz:
                print(f"[ {row} ]")
            print("\n")
        else:
            # insertar el id en la matriz de acuerdo a la posicion recibida
            self.game.matriz[x][y] = cliente_id
            print("\n")
            for row in self.game.matriz:
                print(f"[ {row} ]")
            print("\n")
            print("tiro en x: " + str(x) + " y: " + str(y))
            siguiente_turno = 1 if self.game.bandera_turno else 0

            message = json.dumps({ "turno": siguiente_turno, "matriz": self.game.matriz })
            print("turno: " + str(siguiente_turno))
            time.sleep(1)
            self.game.clients_arr[siguiente_turno].write_message(message)
            
            self.game.bandera_turno = not self.game.bandera_turno  # cambio de turno 
        
    # Se ejecuta cuando se cierra la conexión del cliente
    def on_close(self):
        print ("Un agente ha dejado el campo de batalla")

application = tornado.web.Application([(r"/", EchoWebSocket),])
print("Servidor funcionando en el puerto 9000")
application.listen(9000)
tornado.ioloop.IOLoop.instance().start()
