
from datetime import datetime
from random import randint
import requests
import json
import time
# from ISStreamer.Streamer import Streamer

from life import Life
from snake import Snake
from chess import Chess

#from sense_emu import SenseHat
from sense_hat import SenseHat

API_KEY = '4628a260600466967c04cf9974306321'
LAT = -36.87
LON = 174.77
EXCLUDE = ''
URL = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude{}&appid={}'

ACCESS_KEY = ""
BUCKET_KEY = "DYCKPSMEJ57P"
BUCKET_NAME = "Office"

# My Weather app. Polls OpenWeatherMap.org to get forecasts for Auckland, and then displays 8
# days of weather icons, followed by a map of the next 8 days showing basic weather and chance of rain.
# Then for entertainment it drops into Life, Snake or Chess before repeating. Runs on a SenseHat in a nice
# wooden frame in my study. Forecasts seem pretty good too.
#
# https://simongarton.com/docs/projects/post-2020-11-24-raspberry-pi/
#
# Simon Garton
# simon.garton@gmail.com
# November / December 2020


class WeatherReport():

    def get_time(self, unix):
        return datetime.fromtimestamp(unix)

    def get_temp(self, kelvin):
        return '{}C'.format(round(kelvin - 273.15))

    def get_temp_detail(self, temp):
        detail = {}
        detail['day'] = '{}C'.format(round(temp['day'] - 273.15))
        detail['min'] = '{}C'.format(round(temp['min'] - 273.15))
        detail['max'] = '{}C'.format(round(temp['max'] - 273.15))
        detail['night'] = '{}C'.format(round(temp['night'] - 273.15))
        detail['eve'] = '{}C'.format(round(temp['eve'] - 273.15))
        detail['morn'] = '{}C'.format(round(temp['morn'] - 273.15))
        return detail

    def get_feels_like_detail(self, temp):
        detail = {}
        detail['day'] = '{}C'.format(round(temp['day'] - 273.15))
        detail['night'] = '{}C'.format(round(temp['night'] - 273.15))
        detail['eve'] = '{}C'.format(round(temp['eve'] - 273.15))
        detail['morn'] = '{}C'.format(round(temp['morn'] - 273.15))
        return detail

    def __init__(self, data, detailed):
        self.raw_data = data
        self.time = self.get_time(data['dt'])
        self.sunrise = self.get_time(
            data['sunrise']) if 'sunrise' in data else None
        self.sunset = self.get_time(
            data['sunset']) if 'sunset' in data else None
        if detailed:
            self.temp = self.get_temp_detail(data['temp'])
        else:
            self.temp = self.get_temp(data['temp'])
        if detailed:
            self.feels_like = self.get_feels_like_detail(data['feels_like'])
        else:
            self.feels_like = self.get_temp(data['feels_like'])
        self.dew_point = self.get_temp(data['dew_point'])
        self.pressure = '{}mBar'.format(data['pressure'])
        self.humidity = '{}%'.format(data['humidity'])
        self.uvi = '{}'.format(data['uvi']) if 'uvi' in data else None
        self.clouds = '{}%'.format(data['clouds'])
        self.wind_speed = '{}kts'.format(data['wind_speed'])
        self.wind_deg = '{}°'.format(data['wind_deg'])
        # can be more than 1
        self.weather = '{}'.format(data['weather'][0]['main'])
        self.description = '{}'.format(data['weather'][0]['description'])
        # could format, but then harder to work with later
        self.pop = data['pop'] if 'pop' in data else None
        self.rain = data['rain'] if 'rain' in data else None
        self.snow = data['snow'] if 'snow' in data else None


class Weather():

    def __init__(self):
        self.sense = SenseHat()
        self.sense.clear()
        self.sense.low_light = True

    def get_data(self):
        url = URL.format(LAT, LON, EXCLUDE, API_KEY)
        print(datetime.now(), url)
        data = requests.get(url)
        if data.status_code != 200:
            print('failed with ' + data.status_code)
            return None
        return data.json()

    def get_time(self, unix):
        return datetime.fromtimestamp(unix)

    def current(self, data):
        weatherReport = WeatherReport(data, False)
        return weatherReport

    def hourly(self, hourly):
        data = []
        for hour in hourly:
            weatherReport = WeatherReport(hour, False)
            data.append(weatherReport)
        return data

    def daily(self, daily):
        data = []
        for day in daily:
            weatherReport = WeatherReport(day, True)
            data.append(weatherReport)
        return data

    def minutely(self, minutely):
        data = []
        for minute in minutely:
            time = self.get_time(minute['dt'])
            precipitation = minute['precipitation']
            data.append([time, precipitation])
        return data

    def getData(self, makeCall):
        if makeCall:
            response = self.get_data()
            with open('response-live.json', 'w') as output:
                json.dump(response, output)
        else:
            with open('response.json', 'r') as input:
                response = json.load(input)
        response['current'] = self.current(response['current'])
        response['minutely'] = self.minutely(
            response['minutely']) if 'minutely' in response else {}
        response['hourly'] = self.hourly(response['hourly'])
        response['daily'] = self.daily(response['daily'])
        # self.dump(response['current'])
        # print(len(response['minutely']))
        # print(len(response['hourly']))
        # print(len(response['daily']))
        return response

    def displayWeatherAsText(self, weather):
        self.sense.show_message(weather)

    def displayIcon(self, dayIndex, weather):
        icons = {
            "Clouds": self.getCloudsIcon(),
            "Clear": self.getClearIcon(),
            "Rain": self.getRainIcon()
        }
        if not weather in icons:
            self.displayWeatherAsText(weather)
            return
        self.sense.set_pixels(icons[weather])
        #self.sense.set_pixel(dayIndex, 7, [255, 255, 255])

    def getClearIcon(self):
        b = [0, 0, 0]
        f = [255, 255, 0]
        pixels = [
            b, b, b, b, b, b, b, b,
            b, b, b, f, f, b, b, b,
            b, b, f, f, f, f, b, b,
            b, f, f, f, f, f, f, b,
            b, f, f, f, f, f, f, b,
            b, b, f, f, f, f, b, b,
            b, b, b, f, f, b, b, b,
            b, b, b, b, b, b, b, b
        ]
        return pixels

    def getCloudsIcon(self):
        b = [0, 0, 0]
        f = [255, 255, 255]
        pixels = [
            b, b, b, b, b, b, b, b,
            b, b, b, f, f, b, b, b,
            b, b, f, f, f, f, f, b,
            b, f, f, f, f, f, f, f,
            f, f, f, f, f, f, f, f,
            b, b, f, f, f, f, f, b,
            b, b, b, b, b, b, b, b,
            b, b, b, b, b, b, b, b
        ]
        return pixels

    def getRainIcon(self):
        b = [0, 0, 0]
        f = [100, 100, 100]
        r = [0, 0, 200]
        pixels = [
            b, b, b, b, b, b, b, b,
            b, b, b, f, f, b, b, b,
            b, b, f, f, f, f, f, b,
            b, f, f, f, f, f, f, f,
            f, f, f, f, f, f, f, f,
            b, b, f, f, f, f, f, b,
            b, b, b, r, b, b, r, b,
            b, b, b, b, r, b, b, r
        ]
        return pixels

    def get_color(self, weather):
        colors = {
            "Clouds": [200, 200, 200],
            "Clear": [255, 255, 0],
            "Rain": [100, 100, 100]
        }
        if not weather in colors:
            return [255, 0, 0]
        return colors[weather]

    def display_week(self, daily):
        a = 0
        for day in daily:
            weather = day.weather
            color = self.get_color(weather)
            #print(day.time, weather, day.pop)
            self.sense.set_pixel(a, 4, color)
            self.sense.set_pixel(a, 5, color)
            self.sense.set_pixel(a, 6, color)
            self.sense.set_pixel(a, 7, color)
            pop = round(day.pop * 4)
            for b in range(4 - pop, 4):
                self.sense.set_pixel(a, b, [0, 0, 255])
            a = a + 1
        pass

    def heart(self):
        pixels = [
            [0, 1, 1, 0, 0, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
        start_time = time.time()
        self.sense.clear()
        while(True):
            for bright in range(0, 127):
                self.draw(bright * 2, pixels)
            for bright in range(127, 0, -1):
                self.draw(bright * 2, pixels)
            if (time.time() - start_time) > 30:
                break

    def draw(self, bright, pixels):
        for row in range(0, 8):
            for col in range(0, 8):
                if pixels[col][row] == 1:
                    self.sense.set_pixel(row, col, (bright, 0, 0))

    # def uploadTempHumidityDataToIS(self):
    #     streamer = Streamer(bucket_name=BUCKET_NAME,
    #                         bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)
    #     temp = round(self.sense.get_temperature_from_humidity(), 1)
    #     streamer.log("temperature", temp)
    #     humidity = round(self.sense.get_humidity(), 0)
    #     streamer.log("humidity", humidity)
    #     streamer.flush()
    #     print("temp {} humidity {}".format(temp, humidity))

    # def uploadPressureDataToIS(self):
    #     streamer = Streamer(bucket_name=BUCKET_NAME,
    #                         bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)
    #     pressure = round(self.sense.get_pressure(), 1)
    #     streamer.log("pressure", pressure)
    #     streamer.flush()
    #     print("pressure {}".format(pressure))

    def display(self, makeCall):
        call = time.time()
        while(True):
            data = self.getData(makeCall)
            # self.uploadTempHumidityDataToIS()
            # self.uploadPressureDataToIS()
            # 8 days * 3 seconds = 24 seconds * 10 = 4 minutes * 15 = 1 hour
            for l in range(0, 10 * 15):
                i = 0
                for day in data['daily']:
                    #print('{} {}:{}'.format(i, day.time, day.weather))
                    self.displayIcon(i, day.weather)
                    time.sleep(1)
                    self.sense.clear()
                    time.sleep(0.2)
                    i = i + 1
                time.sleep(2)
                self.display_week(data['daily'])
                time.sleep(5)
                now = time.time()
                if (now - call) > 60 * 5:
                    # self.uploadTempHumidityDataToIS()
                    call = time.time()
                if (l % 4 == 3):
                    life = Life()
                    life.run(8, 8, 30)
                if (l % 4 == 1):
                    snake = Snake()
                    try:
                        snake.run(30)
                    except Exception as e:
                        print(e)
                if (l % 4 == 2):
                    self.heart()
                if (l % 4 == 0):
                    chess = Chess()
                    chess.play()
                self.sense.clear()
                time.sleep(5)

    def dump(self, obj):
        for attr in dir(obj):
            if '__' in '{}'.format(attr):
                continue
            if '<bound' in '{}'.format(getattr(obj, attr)):
                continue
            print("obj.%s = %r" % (attr, getattr(obj, attr)))


weather = Weather()
weather.display(True)
