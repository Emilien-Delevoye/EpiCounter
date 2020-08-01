import json


class InitData:
    def __init__(self):
        self.__dict__ = {}

    def read_config_file(self):
        with open("config.json", "r") as file:
            self.__dict__ = json.load(file)
        file.close()

    def get_dict(self):
        return self.__dict__

    def get_room_names(self):
        return list(self.__dict__.keys())
