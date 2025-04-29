import pandas as pd
import socket
import rsa
import json


class UserManager:
    def __init__(self):
        self.users = pd.read_csv("users.csv")
    
    def regestration(self, login, password, staffRights):
        if login not in self.users["login"]:
            self.users.loc[self.users.shape[0]] = [login, password, "0"*(12-int(len(str(self.users.shape[0])))) + str(self.users.shape[0]), staffRights]
            return True
        else:
            return False
        
        self.users.to_csv("users.csv")
        
    def login(self, login, password):
        if login in self.users["login"] and password == self.users[self.users["login"] == login]["password"]:
            return True
        else:
            return False

class OrderManager:
    def __init__(self):
        self.orders = pd.read_csv("orders.csv")
    
    def addOrder(self, orderId, carriageNumber, placeNumber, dishesId, status):
        self.orders.loc[self.orders.shape[0]] = [orderId, carriageNumber, placeNumber, dishesId, status]
        self.orders.to_csv("orders.csv")
        return True

class Server:
    def __init__(self, host, port):
        self.keys = pd.read_csv("keys.csv", index_col="addr")
        self.sock = socket.socket()
        self.sock.bind((host, port))
        self.sock.listen(1)
        
        self.um = UserManager()
        self.om = OrderManager()

    def managerRequest(self):
        client_socket, addr = self.sock.accept()
        data = client_socket.recv(4096)
        if data.decode() == "1":
            (publicKey, closedKey) = rsa.newkeys(4096)
            if addr not in self.keys["addr"]:
                self.keys.loc[self.keys.shape[0]] = [addr, publicKey, closedKey]
                client_socket.send(self.keys[addr][1])
            else:
                self.keys[addr] = [addr, publicKey, closedKey]

        data = rsa.decrypt(data, self.keys[addr][2])
        data = json.loads(data.decode())
        
        if data["action"] == "register":
            client_socket.send(self.um.regestration(data["login"], data["password"], data["staffRight"]))

        if data["action"] == "login":
            client_socket.send(self.um.login(data["login"], data["password"]))

        if data["action"] == "order":
            client_socket.send(self.om.addOrder(data["orderId"], data["carriageNumber"], data["placeNumber"], data["dishesId"], data["status"]))
        






        
