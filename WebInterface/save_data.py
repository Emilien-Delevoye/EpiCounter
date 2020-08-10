from WebInterface.use_functions import get_file_name
from datetime import datetime
from threading import Thread
import json


class SaveData(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server

    def run(self):
        current = False
        while True:
            date = datetime.now()
            if date.second % 30 == 0 and current is False and (date.hour >= 8 or date.hour < 2):
                current = True
                data = self.server.get_data()
                try:
                    with open("data/" + get_file_name(), "r") as file:
                        tmp = json.load(file)
                        file.close()
                    with open("data/" + get_file_name(), "w") as file:
                        tmp[datetime.now().strftime("%d/%m/%Y %H:%M:%S")] = data
                        file.write(str(json.dumps(tmp, indent=1)))
                        file.close()
                except FileNotFoundError:
                    pass
                    with open("data/" + get_file_name(), "w") as file:
                        tmp = {datetime.now().strftime("%d/%m/%Y %H:%M:%S"): data}
                        file.write(str(json.dumps(tmp, indent=1)))
                        file.close()
            elif date.second % 30 != 0 and current is True:
                current = False
