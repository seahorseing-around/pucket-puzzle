from gpiozero import LED, Button
from signal import pause

class Butt:
    def __init__(self, led_pin,button_pin,id,roman):
        self.led = LED(led_pin)
        self.button = Button(button_pin)
        self.id = id
        self.roman = roman
    
    def wait_button(self):
        self.button.wait_for_press()

buttons = [
    # Butt(led_pin, button_pin, id, Roman Numeral)
    Butt(20, 21, 1, "L"), # white, green
    Butt(12, 16, 2, "X2"), # red, yellow
    Butt(15, 1, 3, "X4"), # blue, *white* - wrong wire

    Butt(19, 26, 4, "I1"), # blue, black
    Butt(6, 13, 5, "I4"), # yellow, red
    Butt(5, 0, 6, "I3"), # green, white

    Butt(22, 10, 7, "I2"), # yellow, red
    Butt(9, 11, 8, "V"), # blue, black
    Butt(27, 17, 9, "X3"), # green, white ** problem

    Butt(24, 25, 10, "X1"), # red, yellow
    Butt(8, 7, 11, "High Score"), # white, green
    Butt(18, 23, 12, "C") # black, blue
]


for b in buttons:
    b.button.when_pressed = b.led.on



    b.button.when_released = b.led.off

pause()