from gpiozero import Button, LED, DigitalInputDevice, OutputDevice
from time import sleep
from signal import pause
import time
import logging
from signal import signal, SIGTERM, SIGINT
from sys import exit
import random
import configparser
import threading


#TODO work out useful info logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

SOLENOID = OutputDevice(14)


if __name__ == '__main__':

    while True:
        print("Solenoid Open")
        SOLENOID.on()
        sleep(3)
        print("Solenoid Close")
        SOLENOID.off()
        sleep(3)

    