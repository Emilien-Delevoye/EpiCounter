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
            if datetime.now().second % 30 == 0 and current is False:
                current = True
                data = self.server.get_data()
                try:
                    with open("data/" + datetime.now().strftime("%d-%m-%Y") + ".json", "r") as file:
                        tmp = json.load(file)
                        file.close()
                    with open("data/" + datetime.now().strftime("%d-%m-%Y") + ".json", "w") as file:
                        tmp[datetime.now().strftime("%d/%m/%Y %H:%M:%S")] = data
                        file.write(str(json.dumps(tmp, indent=1)))
                        file.close()
                except FileNotFoundError:
                    pass
                    #Faire ce qu'il manque dans cette fonction, dans le cas d'un nouveau fichier
                    with open("data/" + datetime.now().strftime("%d-%m-%Y") + ".json", "w") as file:
                        print("pouet")
                        file.write(str(json.dumps(data, indent=1)))
                        file.close()
            elif datetime.now().second % 30 != 0 and current is True:
                current = False
