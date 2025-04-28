import pandas as pd
import socket

class UserManager:
    def __init__(self):
        self.users = pd.read_csv("server/users.csv")

    def registration(self, login, password, staffRights):
        if login not in self.users["login"]:
            self.users.loc[self.users.shape[0]] = [login, password, "0"*(12-int(len(str(self.users.shape[0])))) + str(self.users.shape[0]), staffRights]
            self.users.to_csv("server/users.csv")
            return True
        else:
            return False



    def login(self, login, password):
        if login in self.users["login"] and password == self.users[self.users["login"] == login]["password"]:
            return True
        else:
            return False

class OrderManager:
    def __init__(self):
        self.orders = pd.read_csv("server/orders.csv")
    
    def addOrder(self, orderId, carriageNumber, placeNumber, dishesId, status):
        self.orders.loc[self.orders.shape[0]] = [orderId, carriageNumber, placeNumber, dishesId, status]
        self.orders.to_csv("server/orders.csv")

class Server:
    def __init__(self, host, port):
        self.sock = socket.socket()
        self.sock.bind((host, port))
        self.sock.listen(100)
        
        self.um = UserManager()
        self.om = OrderManager()

    def managerRequest(self):
        client_socket, addr = self.sock.accept()
        data = client_socket.recv(2048)
        data = data.split()
        if data[0] == "registrarion":
            client_socket.send(f"{self.um.registration(data[1], data[2], data[3])}".encode())

        if data[0] == "login":
            client_socket.send(f"{self.um.login(data[1], data[2])}".encode())

        if data[0] == "order":
            client_socket.send(f"{self.om.addOrder(data[1], data[2], data[3], data[4], data[5])}".encode())
        
