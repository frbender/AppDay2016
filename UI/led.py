""" LEDs ein- und ausschalten"""

import threading
import time

import RPi.GPIO


class LedHandler(threading.Thread):
    on = True
    Lock = threading.Lock

    def __init__(self, color: bool):
        threading.Thread.__init__(self)
        self.gpio = 0
        if color:
            self.gpio = 31
        else:
            self.gpio = 37
        # Pins setzen
        RPi.GPIO.setmode(RPi.GPIO.BOARD)

        # OUT ist der Ausgang; LOW steht fuer 0 Volt
        RPi.GPIO.setup(self.gpio, RPi.GPIO.OUT)
        RPi.GPIO.output(self.gpio, RPi.GPIO.LOW)

    def run(self):
        while self.on:
            RPi.GPIO.output(self.gpio, RPi.GPIO.HIGH)
            time.sleep(0.2)
            RPi.GPIO.output(self.gpio, RPi.GPIO.LOW)
            time.sleep(0.2)
        RPi.GPIO.cleanup()