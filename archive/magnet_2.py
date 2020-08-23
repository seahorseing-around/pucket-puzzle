from gpiozero import LED, DigitalInputDevice
from signal import pause

led = LED(27)
sensor = DigitalInputDevice(24)

def on_led():
    print("on Detected")
    led.on()

def off_led():
    print("off detected")
    led.off()

sensor.when_activated = on_led

sensor.when_deactivated = off_led

pause()