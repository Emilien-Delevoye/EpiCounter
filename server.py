from Server.Server import Server
from flask import Flask
from multiprocessing import Process


app = Flask("EpiCounter")


@app.route("/")
def pouet():
    return "Hello"


def mainServer():
    server = Server()
    server.open()
    try:
        server.run()
    except KeyboardInterrupt:
        server.close()
        print("Server closed by Ctrl C")
        return
    server.close()


def mainFlask():
    app.run("0.0.0.0", 4242)


if __name__ == "__main__":
    p1 = Process(target=mainServer)
    p2 = Process(target=mainFlask)
    p1.start()
    p2.start()
