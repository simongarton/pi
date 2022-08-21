import requests
import time

from sense_hat import SenseHat
#from sense_emu import SenseHat

# Start of a tool to monitor my Kung Fu student database to display activity. Not complete.
#
# Simon Garton
# simon.garton@gmail.com
# November / December 2020

LOCAL_HOST = 'http://localhost:8082/metrics'

PRODUCTION = 'https://api.nzkungfuschool.com/metrics'

FACE_PIXELS = [
    [0, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 0, 1],
    [0, 1, 1, 1, 1, 1, 1, 0]]


class Monitor():

    def __init__(self):
        self.sense = SenseHat()
        self.sense.clear()
        print(self.sense)

    def show_error(self):
        for row in range(0, 8):
            for col in range(0, 8):
                if FACE_PIXELS[col][row] == 1:
                    self.sense.set_pixel(row, col, (255, 0, 0))
        time.sleep(10)
        self.sense.clear()
        time.sleep(3)

    def belt_colors(self, json):
        colors = ['White', 'Yellow', 'Green', 'Blue', 'Brown', 'Black']
        counts = {}
        for color in colors:
            counts[color] = 0
        for count in json['gradeCounts']:
            for color in colors:
                if color in count['grade']:
                    counts[color] = counts[color] + 1
                if 'Dan' in count['grade']:
                    counts['Black'] = counts['Black'] + 1
        results = []
        max = 0
        total = 0
        for color in colors:
            results.append([color, counts[color]])
            total = total + counts[color]
            if counts[color] > max:
                max = counts[color]

        print("belt colors", results)
        self.sense.clear()
        led_colors = [
            [255, 255, 255],
            [255, 255, 0],
            [255, 255, 0],
            [0, 0, 255],
            [140, 70, 20],
            [50, 50, 50]
        ]
        for x in range(0, 6):
            y = int(results[x][1] * 7.0 / max)
            if results[x][1] == 0:
                continue
            for y1 in range(0, y + 1):
                self.sense.set_pixel(x + 1, 7 - y1, led_colors[x])

        return results

    def run(self):
        while True:
            self.sense.clear()
            try:
                resp = requests.get(PRODUCTION)
            except requests.exceptions.ConnectionError as e:
                print(e)
                self.show_error()
                continue
            json = resp.json()
            self.belt_colors(json)
            # print(json)
            time.sleep(10)


monitor = Monitor()
monitor.run()
