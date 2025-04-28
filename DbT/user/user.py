import socket

#написть декоратор для шифрования

class Client:
    def __init__(self, host, port):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((host, port))

class Authorization(Client):
    def registrarion(self, login, password, staffRights = False):
        self.clientSocket.send(f"{"registrarion"} {login} {password} {staffRights}".encode())

    def login(self, login, password):
        self.clientSocket.send(f"{"login"} {login} {password}".encode())

class OrderManager(Client):
    def SendOrder(self, orderId, carriageNumber, placeNumber, dishesId, status = "notStarted"):
        self.clientSocket.send(f"{"order"} {orderId} {carriageNumber} {placeNumber} {dishesId} {status}".encode())