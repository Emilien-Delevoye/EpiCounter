import socket


class Server:
    def __init__(self):
        print("Server init")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def open(self):
        self.socket.bind(('localhost', 4242))
        self.socket.listen(5)

    def close(self):
        self.socket.close()
