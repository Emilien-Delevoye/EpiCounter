from threading import Thread
import socket
from datetime import datetime
import json


class Server(Thread):
    def __init__(self, init):
        Thread.__init__(self)
        self.__source__ = init.get_dict()
        self.database = {}
        for i in self.__source__:
            self.database[i] = dict()
            self.database[i]["total"] = 0
            for j in self.__source__[i]:
                self.database[i][j] = [0, 0]
        try:
            filename = "data/" + datetime.now().strftime("%d-%m-%Y") + ".json"
            with open(filename, "r") as file:
                tmp = json.load(file)
                last = tmp[list(tmp.keys())[-1]]
                for i in last:
                    self.database[i] = last[i]
            file.close()
        except FileNotFoundError:
            pass
        print(self.database)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("localhost", 4242))
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                data = data.decode("utf-8")
                data = data.split("\n")[0]
                data = data.split("|")
                print(data)
                if len(data) != 3:
                    raise ValueError
                if data[0] not in self.database.keys() or data[1] not in self.database[data[0]].keys():
                    raise Exception
                else:
                    if data[2] == "+1":
                        self.database[data[0]][data[1]][0] += 1
                        self.database[data[0]]["total"] += 1
                    elif data[2] == "-1" and self.database[data[0]]["total"] > 0:
                        self.database[data[0]][data[1]][1] += 1
                        self.database[data[0]]["total"] -= 1
                    else:
                        raise ValueError
                    print(self.database)
            except:
                print("Message ignoré (Erreur de réception)")

    def get_data(self):
        return self.database
