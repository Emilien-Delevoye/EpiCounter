from flask import Flask, send_from_directory, jsonify, request
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from datetime import datetime
from WebInterface.server import Server
import os


app = Flask(__name__)
a = Server()


def read_file():
    filename = "data/" + datetime.now().strftime("%d-%m-%Y") + ".txt"
    current_date = None
    all_data = {}
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        return None
    for i in file:
        if i[0] == '=':
            current_date = datetime.strptime(i, "=== %d/%m/%Y %H:%M:%S ===\n").strftime("%d/%m/%Y %H:%M:%S")
            all_data[current_date] = {}
        else:
            room_data = i.split('|')
            all_data[current_date][room_data[0]] = room_data[1][:-1]
    file.close()
    return all_data


def create_plot(room, new_data):
    times = [datetime.strptime(line, "%d/%m/%Y %H:%M:%S") for line in new_data.keys()]
    print(new_data)
    values = [float(line) for line in new_data.values()]
    fig, ax = plt.subplots()
    ax.set_title(room + " : " + times[0].strftime("%d/%m/%Y"))
    ax.set_xlabel("Nombre de personnes")
    ax.set_ylabel("Heure")
    ax.plot_date(times, values, 'k-')
    hfmt = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(hfmt)
    plt.gcf().autofmt_xdate()
    plt.savefig(times[0].strftime("%d-%m-%Y") + ".png", dpi=300)


def return_data(params, room, door):
    new_data = {}
    data = read_file()
    if data is None:
        return "No data found"
    for i in data.keys():
        if door == 0:
            new_data[i] = data[i][room]
        else:
            new_data[i] = data[i][room + "_" + str(door)]
    if door == 0:
        create_plot(room, new_data)
    if params["format"] == "json" and params["current"] is None:
        return jsonify(new_data)
    elif params["format"] == "json" and params["current"] == "true":
        return jsonify(new_data[list(data.keys())[-1]])
    else:
        return "Work in progress"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/cray")
def cray():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Cray", 0)


@app.route("/cray/door_1")
def cray_1():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Cray", 1)


@app.route("/cray/door_2")
def cray_2():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Cray", 2)


@app.route("/knuth")
def knuth():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Knuth", 0)


@app.route("/knuth/door_1")
def knuth_1():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Knuth", 1)


@app.route("/knuth/door_2")
def knuth_2():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Knuth", 2)


@app.route("/knuth/door_3")
def knuth_3():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Knuth", 3)


@app.route("/hamilton")
def hamilton():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Hamilton", 0)


@app.route("/hamilton/door_1")
def hamilton_1():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Hamilton", 1)


@app.route("/hamilton/door_2")
def hamilton_2():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Hamilton", 2)


@app.route("/byron")
def byron():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Byron", 0)


@app.route("/byron/door_1")
def byron_1():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Byron", 1)


@app.route("/byron/door_2")
def byron_2():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Byron", 2)


@app.route("/babbage")
def babbage():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Babbage", 0)


@app.route("/babbage/door_1")
def babbage_1():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Babbage", 1)


@app.route("/pascal")
def pascal():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Pascal", 0)


@app.route("/pascal/door_1")
def pascal_1():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Pascal", 1)


@app.route("/turing")
def turing():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Turing", 0)


@app.route("/turing/door_1")
def turing_1():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Turing", 1)


@app.route("/")
def home():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    return return_data(params, "Cray", 0)


def main():
    a.start()
    app.run()


if __name__ == "__main__":
    main()
