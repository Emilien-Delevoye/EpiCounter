from flask import Flask, send_from_directory, jsonify, request, render_template
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from datetime import datetime
from WebInterface.server import Server
from WebInterface.save_data import SaveData
from WebInterface.init_data import InitData
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


def read_file():
    try:
        with open("data/" + datetime.now().strftime("%d-%m-%Y") + ".json", "r") as file:
            all_data = json.load(file)
    except FileNotFoundError:
        return None
    return all_data


def create_plot(room_name, new_data):
    times = [datetime.strptime(line, "%d/%m/%Y %H:%M:%S") for line in new_data.keys()]
    print(new_data)
    values = [float(line) for line in new_data.values()]
    fig, ax = plt.subplots()
    ax.set_title(room_name + " : " + times[0].strftime("%d/%m/%Y"))
    ax.set_xlabel("Nombre de personnes")
    ax.set_ylabel("Heure")
    ax.plot_date(times, values, 'k-')
    hfmt = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(hfmt)
    plt.gcf().autofmt_xdate()
    plt.savefig(times[0].strftime("%d-%m-%Y") + ".png", dpi=300)


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
    if params["format"] != "json":
        create_plot(room_name, new_data)
    if params["format"] == "json" and params["current"] is None:
        return jsonify(new_data)
    elif params["format"] == "json" and params["current"] == "true":
        return jsonify(new_data[list(data.keys())[-1]])
    else:
        return "Work in progress"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/rooms", methods=['GET'])
def rooms():
    return jsonify(init.get_room_names())


@app.route("/<room_name>/")
def room(room_name):
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    try:
        return return_data(params, str(room_name))
    except:
        return "Wrong name"


@app.route("/")
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
    app.run()


if __name__ == "__main__":
    main()
