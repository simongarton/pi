from sense_hat import SenseHat
from datetime import datetime

sense = SenseHat()

red = (255, 0, 0)
blue = (0, 0, 255)
white = (200, 200, 200)
black = (0, 0, 0)


while True:

    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    print(now)
    sense.show_message(now, text_colour=black, back_colour=white)

    temp = sense.get_temperature()
    temp = round(temp * 10) / 10
    temp = str(temp) + 'C'
    print(temp)
    sense.show_message(temp, text_colour=red)

    humidity = sense.get_humidity()
    humidity = round(humidity * 10) / 10
    humidity = str(humidity) + '%'
    print(humidity)
    sense.show_message(humidity, text_colour=blue)

    pressure = sense.get_pressure()
    pressure = round(pressure * 10) / 10
    pressure = str(pressure) + 'mbar'
    print(pressure)
    sense.show_message(pressure, text_colour=white)
