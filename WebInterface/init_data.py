import json


class InitData:
    def __init__(self):
        self.__dict__ = {"1": {}, "2": {}}

    def read_config_file(self):
        with open("config.json", "r") as file:
            self.__dict__["1"] = json.load(file)
        file.close()
        for i in list(self.__dict__["1"].keys()):
            self.__dict__["2"][i] = self.__dict__["1"][i][0]
        for i in list(self.__dict__["1"].keys()):
            del self.__dict__["1"][i][0]

    def get_dict(self):
        return self.__dict__["1"]

    def get_room_max(self):
        return self.__dict__["2"]

    def get_room_names(self):
        return list(self.__dict__["1"].keys())
