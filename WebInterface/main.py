from flask import Flask, send_from_directory, jsonify, request, render_template, redirect, session
from datetime import datetime
from WebInterface.server import Server
from WebInterface.save_data import SaveData
from WebInterface.init_data import InitData
from WebInterface.create_plot import CreatePlot
from WebInterface.login_check import check_login
import json
import time
import os


app = Flask(__name__)
app.secret_key = "admin"
app.url_map.strict_slashes = False
init = InitData()
try:
    init.read_config_file()
except FileNotFoundError:
    exit(1)
print(init.get_dict())
address = "http://0.0.0.0"
port = ":4243"
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


def return_data(params, room_name, account):
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
        return render_template('room_display.html', Title=room_name, account=account)


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/login/")
def login():
    return render_template("login.html")


@app.route("/dologin", methods=['POST'])
def dologin():
    if check_login(request.form["username"], request.form["password"]):
        session["logged_in"] = True
        session["username"] = request.form["username"]
        return redirect(address + port)
    else:
        return "ko"


@app.route("/profile/")
def profile():
    try:
        if session["logged_in"] is not True:
            return redirect(address + port + "/login/")
        else:
            return render_template("profile.html", Name=session["username"])
    except KeyError:
        return redirect(address + port + "/login")


@app.route("/status")
def status():
    if "logged_in" not in session or session["logged_in"] is not True:
        return redirect(address + port + "/unauthorized")
    else:
        if request.values.get('format') == "json":
            output = {}
            for i in server.database_status:
                output[i] = {}
                for j in server.database_status[i]:
                    if server.database_status[i][j] is None or datetime.fromtimestamp(time.time() - 30) > server.database_status[i][j]:
                        output[i][j] = False
                    else:
                        output[i][j] = True
            return jsonify(output)
        else:
            return render_template("status.html")


@app.route("/logout/")
def logout():
    session["logged_in"] = False
    session.pop("username", None)
    return redirect(address + port)


@app.route("/unauthorized/")
def unauthorized():
    return render_template("unauthorized.html")


@app.route("/rooms", methods=['GET'])
def rooms():
    return jsonify(init.get_room_names())


@app.route("/rooms_max", methods=['GET'])
def rooms_max():
    return jsonify(init.get_room_max())


@app.route("/<room_name>/set", methods=['GET'])
def room_set(room_name):
    if room_name not in server.database:
        return "Room not found"
    params = dict()
    params["newval"] = request.values.get('newval')
    if "logged_in" not in session or session["logged_in"] is not True:
        return redirect(address + port + "/unauthorized")
    try:
        if params["newval"] is not None:
            server.database[room_name]["total"] = int(params["newval"])
            return redirect(address + port + room_name + "/set")
    except ValueError:
        return "Wrong parameter \"newval\""
    return render_template("room_set.html", room_name=room_name)


@app.route("/<room_name>/", methods=['GET'])
def room(room_name):
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    try:
        if "logged_in" in session and session["logged_in"] is True:
            return return_data(params, str(room_name), "Set number")
        return return_data(params, str(room_name), "")
    except:
        return "Wrong name"


@app.route("/", methods=['GET'])
def home():
    params = dict()
    params["format"] = request.values.get('format')
    params["current"] = request.values.get('current')
    if params["format"] == "json" and params["current"] == "true":
        new_base = {}
        max_rooms = server.init.get_room_max()
        try:
            for i in server.database:
                new_base[i] = list()
                new_base[i].append(server.database[i]["total"])
                new_base[i].append(max_rooms[i])
            return jsonify(new_base)
        except EOFError:
            return jsonify({})
    else:
        if "logged_in" in session and session["logged_in"] is True:
            return render_template('index.html', statut="logout", statut_disp="Logout", name=session["username"])
        else:
            return render_template('index.html', statut="login", statut_disp="Login", name="")


def main():
    server.start()
    savedata.start()
    plot.start()
    app.run()


if __name__ == "__main__":
    main()
