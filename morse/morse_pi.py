import requests
import json
import os

import RPi.GPIO as GPIO
import time
from morse import Morse

SHORT = 0.2
LONG = 0.6
SPACE = 1

PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN, GPIO.OUT)


API_KEY = '9cdefeafe3c147ea9e7f316fb25b04f2'

morse = Morse()


def on():
    GPIO.output(PIN, GPIO.HIGH)
    pass


def off():
    GPIO.output(PIN, GPIO.LOW)
    pass


def flash(s):
    for c in s:
        flash_one(c)
    time.sleep(SPACE)


def flash_one(s):
    print(s)
    if s == ' ':
        time.sleep(SPACE)
        return
    if s == '.':
        on()
        time.sleep(SHORT)
        off()
        time.sleep(LONG)
        return
    if s == '-':
        on()
        time.sleep(LONG)
        off()
        time.sleep(SHORT)
        return
    print('can\'t flash {}'.format(s))


def flash_message(message):
    for c in message:
        s = morse.cipher(c)
        flash(s)


def simple():
    message = 'Hello world'
    print(morse.encode(message))
    flash_message(message)


def news():
    response = requests.get(
        'https://newsapi.org/v2/top-headlines?apiKey={}&country=nz'.format(API_KEY))
    data = response.text
    news = json.loads(data)
    articles = news['articles']
    while True:
        for article in articles:
            title = article['title']
            print(title)
            flash_message(title)


if __name__ == '__main__':
    os.remove('output.txt')
    news()
