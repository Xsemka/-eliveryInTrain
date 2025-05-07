import socket
import json
import rsa



class Client:
    def __init__(self, host, port):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((host, port))
        self.clientSocket.send("1".encode())
        self.publicKey = self.clientSocket.recv(4096)

class Authorization(Client):
    def registrarion(self, login, password, staffRights = False):
        self.clientSocket.send(rsa.encrypt(json.dumps({"action":"registrarion", "login":login, "password":password, "staffRights":staffRights}, ensure_ascii=False, indent=2).encode(), self.publicKey))

    def login(self, login, password):
        self.clientSocket.send(json.dumps({"action":"login","login":login, "password":password}, ensure_ascii=False, indent=2).encode())

class OrderManager(Client):
    def SendOrder(self, orderId, carriageNumber, placeNumber, dishesId, status = "notStarted"):
        self.clientSocket.send(json.dumps({"action":"order", "orderId":orderId, "carriageNumber":carriageNumber, "placeNumber":placeNumber, "dishesId":dishesId, "status":status}, ensure_ascii=False, indent=2).encode())





