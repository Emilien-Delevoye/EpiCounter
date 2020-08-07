import json


def check_login(user, password):
    with open("login.json", "r") as file:
        logs = json.load(file)
    try:
        if logs[user] == password:
            return True
        else:
            return False
    except KeyError:
        return False
