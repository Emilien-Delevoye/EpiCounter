from threading import Thread
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import json


class CreatePlot(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server
        self.minute_bf_calc = 10

    def run(self):
        current = False
        while True:
            if datetime.now().minute % self.minute_bf_calc == 0 and datetime.now().second == 10 and current is False:
                print("Start room generation")
                data = self.__read_file__()
                if data is not None:
                    new_data = {}
                    for j in list(data[list(data.keys())[0]].keys()):
                        for i in data.keys():
                            new_data[i] = data[i][j]["total"]
                        self.__create_plot__(j, new_data)
                        new_data = {}
            elif datetime.now().minute % self.minute_bf_calc != 0 and datetime.now().second != 10 and current is True:
                current = False


    def __read_file__(self):
        try:
            with open("data/" + datetime.now().strftime("%d-%m-%Y") + ".json", "r") as file:
                all_data = json.load(file)
            file.close()
        except FileNotFoundError:
            return None
        return all_data

    def __create_plot__(self, room_name, new_data):
        max_rooms = self.server.init.get_room_max()
        times = [datetime.strptime(line, "%d/%m/%Y %H:%M:%S") for line in new_data.keys()]
        values = [float(line) for line in new_data.values()]
        max_values = [float(max_rooms[room_name]) for i in values]
        fig, ax = plt.subplots()
        ax.set_title(room_name + " : " + times[0].strftime("%d/%m/%Y"))
        ax.set_ylabel("Nombre de personnes")
        ax.set_xlabel("Heure")
        ax.plot_date(times, values, 'b-', label="Current")
        ax.plot_date(times, max_values, 'r-', label="Maximum")
        ax.legend()
        hfmt = mdates.DateFormatter('%H:%M:%S')
        ax.xaxis.set_major_formatter(hfmt)
        plt.gcf().autofmt_xdate()
        plt.savefig("static/images/" + room_name + ".png", dpi=300)
        print("Plot for", room_name, "generated")
