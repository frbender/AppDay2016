""" LEDs ein- und ausschalten"""

import RPi.GPIO
import time

class Led():
    # Modulimport
    # RPiGPIO ist fuer die Pins zustaendig
    # Time regelt Zeitabstaende zw. an und aus

    # Funktion mit an, aus, gpio
    def blinken(an : float, aus : float, gpio: int):


        # Pins setzen
        RPi.GPIO.setmode(RPi.GPIO.BOARD)

        # OUT ist der Ausgang; LOW steht fuer 0 Volt
        RPi.GPIO.setup(gpio,RPi.GPIO.OUT)
        RPi.GPIO.output(gpio,RPi.GPIO.LOW)

        # bei jedem Durchlauf der Schleife wird X um 1 erhoeht bis X=1000
        for x in range(1000):
            RPi.GPIO.output(gpio,RPi.GPIO.HIGH)
            time.sleep(an)
            RPi.GPIO.output(gpio,RPi.GPIO.LOW)
            time.sleep(aus)

        # PINs zurueck setzten
        RPi.GPIO.cleanup()

Led.blinken(0.5, 1, 37)