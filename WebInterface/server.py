from threading import Thread
import socket


class Server(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.database = {}

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("localhost", 4242))
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                print("received message: %s" % data.decode('utf-8'))
                print(addr)
                data = data.decode("utf-8")
                data = data.split("\n")[0]
                data = data.split("|")
                if len(data) != 2:
                    raise ValueError
                print(data)
                if data[0] not in self.database.keys():
                    self.database[data[0]] = 0
                    if data[1] == "+1":
                        self.database[data[0]] = 1
                else:
                    if data[1] == "+1":
                        self.database[data[0]] += 1
                    elif data[1] == "-1" and self.database[data[0]] > 0:
                        self.database[data[0]] -= 1
                    else:
                        raise ValueError
                print(self.database)
            except:
                print("Message ignoré (Erreur de réception)")

    def get_data(self):
        return self.database
