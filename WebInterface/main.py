from flask import Flask, send_from_directory, jsonify, request
from datetime import datetime
import os


app = Flask(__name__)


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


def return_data(params):
    data = read_file()
    if data is None:
        return "No data found"
    print(list(data.keys()))
    print(data[list(data.keys())[-1]])
    if params == "json":
        return jsonify(data)
    else:
        return "Work in progress"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/cray")
def cray():
    return "Cray"


@app.route("/cray/door_1")
def cray_1():
    return "Cray door 1"


@app.route("/cray/door_2")
def cray_2():
    return "Cray door 2"


@app.route("/knuth")
def knuth():
    return "Knuth"


@app.route("/knuth/door_1")
def knuth_1():
    return "Knuth door 1"


@app.route("/knuth/door_2")
def knuth_2():
    return "Knuth door 2"


@app.route("/knuth/door_3")
def knuth_3():
    return "Knuth door 3"


@app.route("/hamilton")
def hamilton():
    return "Hamilton"


@app.route("/hamilton/door_1")
def hamilton_1():
    return "Hamilton door 1"


@app.route("/hamilton/door_2")
def hamilton_2():
    return "Hamilton door 2"


@app.route("/byron")
def byron():
    return "Byron"


@app.route("/byron/door_1")
def byron_1():
    return "Byron door 1"


@app.route("/byron/door_2")
def byron_2():
    return "Byron door 2"


@app.route("/babbage")
def babbage():
    return "Babbage"


@app.route("/babbage/door_1")
def babbage_1():
    return "Babbage door 1"


@app.route("/pascal")
def pascal():
    return "Pascal"


@app.route("/pascal/door_1")
def pascal_1():
    return "Pascal door 1"


@app.route("/turing")
def turing():
    return "Turing"


@app.route("/turing/door_1")
def turing_1():
    return "Turing door 1"


@app.route("/")
def home():
    params = request.values.get('format')
    return return_data(params)


def main():
    app.run()


if __name__ == "__main__":
    main()
