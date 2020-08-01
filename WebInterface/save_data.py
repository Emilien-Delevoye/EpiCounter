from threading import Thread
from datetime import datetime
import json


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
                print(data)
                try:
                    with open("data/" + datetime.now().strftime("%d-%m-%Y") + ".json", "r") as file:
                        tmp = json.load(file)
                    with open("data/" + datetime.now().strftime("%d-%m-%Y") + ".json", "w") as file:
                        tmp[datetime.now().strftime("%d/%m/%Y %H:%M:%S")] = data
                        file.write(str(json.dumps(tmp, indent=1)))
                    file.close()
                except FileNotFoundError:
                    pass
                    with open("data/" + datetime.now().strftime("%d-%m-%Y") + ".json", "rw") as file:
                        print("pouet")
                    file.close()
                '''print("salut salut", data)
                for i in data:
                    print(i, data[i])'''
            elif datetime.now().second % 2 != 0 and current is True:
                current = False
