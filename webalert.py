import RPi.GPIO as GPIO
import time
from neopixel import *
import argparse
from webrequest import getTaskSize
from playsound import playsound
#import os, sys 

# LED strip configuration:
LED_COUNT      = 71      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

class tasks:
    def __init__(self):
        self.idamount = getTaskSize()
    def setidamount(self,selfnewamt):
        self.idamount = selfnewamt

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)



GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #TODO look at proper setup
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW) #TODO look at proper setup
GPIO.add_event_detect(11, GPIO.BOTH)
#def my_callback():
#    GPIO.output(13, GPIO.input(11))
#GPIO.add_event_callback(11, my_callback)


if __name__ == '__main__':
#    pygame.mixer.init()
    numTasks = tasks()
    print(numTasks.idamount," is the initial value")
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
#    os.system('omxplayer sound.mp3')
#    sys.exit()

    print ('Press Ctrl-C to quit.')

    try:
        while True:
            #print("output of gpio 11:",GPIO.input(11))
            #test = GPIO.input(11)
            #print(test)
            print(getTaskSize())
            time.sleep(10)
            if not GPIO.input(11):
#                playsound('/home/pi/Downloads/Git/rpi_ws281x/python/examples/sound.mp3')
                #theaterChaseRainbow(strip, 20)
                for i in range(0,5,1):

                    colorWipe(strip, Color(255, 0, 0), 0)
                    time.sleep(1)
                    colorWipe(strip, Color(0, 0, 0), 0)
                    time.sleep(1)
            elif numTasks.idamount < getTaskSize():
                numTasks.setidamount(getTaskSize())
                print("task size increased to ", numTasks.idamount)
#                playsound('sound.mp3')
                for i in range(0,5,1): 
                    colorWipe(strip, Color(255, 0, 0), 0)
                    time.sleep(1)
                    colorWipe(strip, Color(0, 0, 0), 0)
                    time.sleep(1)
            elif numTasks.idamount > getTaskSize():
                numTasks.setidamount(getTaskSize())
#                playsound('sound.mp3')
                print("task size decreased to ", numTasks.idamount)
            else:
                #theaterChaseRainbow(strip, 20)
                colorWipe(strip, Color(0, 0, 0), 0)
    except KeyboardInterrupt:
        GPIO.cleanup()
        colorWipe(strip, Color(0, 0, 0), 0)
