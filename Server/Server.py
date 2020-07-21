import socket
import select
import queue


class Server:
    def __init__(self):
        print("Server init")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverOpen = False
        self.input = [self.socket]
        self.output = list()
        self.messageQueue = {}
        self.buffer = {}
        self.database = {}

    def open(self):
        self.socket.bind(('localhost', 4243))
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

    def __read_data__(self):
        for i in self.buffer:
            a = self.buffer[i].split("\n")
            if a[0]:
                self.__new_cmd__(a[0].split("|"))
            self.buffer[i] = str("")
            for j in a[1:]:
                self.buffer[i] += j

    def __new_cmd__(self, data):
        if data[0] not in self.database:
            self.database[data[0]] = 0
        if data[1] == "+1":
            self.database[data[0]] += 1
        elif data[1] == "-1":
            self.database[data[0]] -= 1
        if self.database[data[0]] < 0:
            self.database[data[0]] = 0
        print(data[0], ":", self.database[data[0]], "(" + data[1] + ")")

    def close(self):
        self.socket.close()
