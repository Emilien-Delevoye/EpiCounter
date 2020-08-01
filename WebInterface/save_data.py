from threading import Thread
from datetime import datetime


class SaveData(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server

    def run(self):
        current = False
        while True:
            if datetime.now().second % 2 == 0 and current is False:
                current = True
                data = self.server.get_data()
                print("salut salut", data)
                for i in data:
                    print(i, data[i])
            elif datetime.now().second % 2 != 0 and current is True:
                current = False

