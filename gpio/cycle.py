import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
valid_ports = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 22, 23]
for i in valid_ports:
    try:
        GPIO.setup(i, GPIO.OUT)
    except ValueError:
        print(i)


while(True):
    for port in valid_ports:
    GPIO.output(port, True)
    time.sleep(0.1)
    GPIO.output(port, False)
    time.sleep(0.1)

GPIO.cleanup()
~
~
