import socket
import select
import queue
from datetime import datetime


class Server:
    def __init__(self):
        print("Server init")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverOpen = False
        self.input = [self.socket]
        self.output = list()
        self.messageQueue = {}
        self.buffer = {}
        self.database = {"Cray": 0, "Cray_1": [0, 0], "Cray_2": [0, 0], "Knuth": 0, "Knuth_1": [0, 0], "Knuth_2": [0, 0],
                         "Knuth_3": [0, 0], "Hamilton": 0, "Hamilton_1": [0, 0], "Hamilton_2": [0, 0],
                         "Byron": 0, "Byron_1": [0, 0], "Byron_2": [0, 0], "Babbage": 0, "Babbage_1": [0, 0],
                         "Pascal": 0, "Pascal_1": [0, 0], "Turing": 0, "Turing_1": [0, 0]}
        self.save_minute = 0

    def open(self):
        self.socket.bind(('127.0.0.1', 4243))
        self.socket.listen(5)
        self.serverOpen = True

    def run(self):
        print("Server running")
        while self.serverOpen:
            readable, writable, expect = select.select(self.input, self.output, self.input, 0)
            for i in readable:
                if i is self.socket:
                    connection, ip = self.socket.accept()
                    connection.setblocking(False)
                    self.input.append(connection)
                    self.messageQueue[connection] = queue.Queue()
                    self.buffer[connection] = str()
                else:
                    try:
                        data = i.recv(1024).decode('utf-8')
                        self.buffer[i] += data
                    except ConnectionResetError:
                        data = None
                    if data:
                        if i not in self.output:
                            self.output.append(i)
                    else:
                        if i in self.output:
                            self.output.remove(i)
                        self.input.remove(i)
                        print("Client with fd", i.fileno(), "is now closed.")
                        i.close()
                        del self.messageQueue[i]
                        del self.buffer[i]
            for i in writable:
                try:
                    next_msg = self.messageQueue[i].get_nowait()
                except queue.Empty:
                    self.output.remove(i)
                else:
                    i.send(next_msg)
            for i in expect:
                self.input.remove(i)
                if i in self.output:
                    self.output.remove(i)
                print("Client with fd ", i.fileno(), " is now closed.")
                i.close()
                del self.messageQueue[i]
                del self.buffer[i]
            self.__read_data__()
            self.__update_database__()

    def __read_data__(self):
        for i in self.buffer:
            a = self.buffer[i].split("\n")
            if a[0]:
                try:
                    self.__new_cmd__(a[0].split("|"))
                except IndexError:
                    print("The message doesn't respect the protocol")
            self.buffer[i] = str("")
            for j in a[1:]:
                self.buffer[i] += j

    def __new_cmd__(self, data):
        if data[0] not in self.database or "_" not in data[0]:
            print("Room not registered")
            return
        if data[1] == "+1":
            self.database[data[0]][0] += 1
            self.database[data[0][:-2]] += 1
        elif data[1] == "-1":
            self.database[data[0]][1] += 1
            self.database[data[0][:-2]] -= 1
        print(data[0], ":", self.database[data[0]], "(" + data[1] + ")", " || ", self.database[data[0][:-2]])

    def __update_database__(self):
        date = datetime.now()
        if date.second % 10 != 0 or date.second == self.save_minute:
            return
        self.save_minute = date.second
        self.__update_file_data__()

    def __update_file_data__(self):
        filename = "WebInterface/data/" + datetime.now().strftime("%d-%m-%Y") + ".txt"
        file = open(filename, "a")
        file.write(datetime.now().strftime("=== %d/%m/%Y %H:%M:%S ===") + "\n")
        for i in self.database:
            file.write(str(i) + "|" + str(self.database[i]) + "\n")
        file.close()

    def close(self):
        self.socket.close()
