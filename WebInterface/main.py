from flask import Flask, send_from_directory, jsonify, request, render_template
from datetime import datetime
from WebInterface.server import Server
from WebInterface.save_data import SaveData
from WebInterface.init_data import InitData
from WebInterface.create_plot import CreatePlot
import json
import os


app = Flask(__name__)
init = InitData()
try:
    init.read_config_file()
except FileNotFoundError:
    exit(1)
server = Server(init)
savedata = SaveData(server)
plot = CreatePlot(server)


def read_file():
    try:
        with open("data/" + datetime.now().strftime("%d-%m-%Y") + ".json", "r") as file:
            all_data = json.load(file)
    except FileNotFoundError:
        return None
    return all_data


def return_data(params, room_name):
    new_data = {}
    if params["current"] == "true":
        return jsonify(server.database[room_name]["total"])
    data = read_file()
    if data is None:
        return "No data found"
    if room_name not in list(data[list(data.keys())[0]].keys()):
        return "Room not found"
    for i in data.keys():
        new_data[i] = data[i][room_name]["total"]
    if params["format"] == "json" and params["current"] is None:
        return jsonify(new_data)
    elif params["format"] == "json" and params["current"] == "true":
        return jsonify(new_data[list(data.keys())[-1]])
    else:
        return render_template('room_display.html', Title=room_name)


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/rooms", methods=['GET'])
def rooms():
    return jsonify(init.get_room_names())


@app.route("/rooms_max", methods=['GET'])
def rooms_max():
    return jsonify(init.get_room_max())


@app.route("/<room_name>/", methods=['GET'])
def room(room_name):
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    try:
        return return_data(params, str(room_name))
    except:
        return "Wrong name"


@app.route("/", methods=['GET'])
def home():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    if params["format"] == "json" and params["current"] == "true":
        new_base = {}
        for i in server.database:
            new_base[i] = server.database[i]["total"]
        return jsonify(new_base)
    else:
        return render_template('index.html')


def main():
    server.start()
    savedata.start()
    plot.start()
    app.run()


if __name__ == "__main__":
    main()
