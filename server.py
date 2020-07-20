from Server.Server import Server


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


if __name__ == "__main__":
    mainServer()
