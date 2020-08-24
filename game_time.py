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

#################
# Configuration #
#################
logging.debug("Open Config File")
config_loc='/home/pi/pucket-puzzle/config.properties'
config = configparser.RawConfigParser()
config.read(config_loc)

high_score = int(config.get('HighScore','high_score'))
game_duration = int(config.get('PucketSection','game_duration'))
winning_score = int(config.get('PucketSection','winning_score'))

logging.info("Config read successfully")
logging.info("High Score: {}".format(high_score))
logging.info("Game Duration: {} seconds".format(game_duration))
logging.info("Winning Score: {}".format(winning_score))

## 11 ## 00 ## 01 ##
## ## 10 ## 02 ## ##
## 09 ## ## ## 03 ##
## ## 08 ## 04 ## ##
## 07 ## 06 ## 05 ##

#HS # C # L #
# # X # X # #
# X # # # X #
# # V # I # #
# I # I # I #


#####################
# Class Definitions #
#####################
def log_press(id):
    logging.debug("Button {} pressed".format(id))

class Butt:
    def __init__(self, led_pin,button_pin,id,roman):
        self.led = LED(led_pin)
        self.button = Button(button_pin)
        self.id = id
        self.roman = roman
    
    def wait_button(self):
        self.button.wait_for_press()

###################
# Pin definitions #
###################
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
    Butt(27,17, 9, "X3"), # green, white ** problem

    Butt(24, 25, 10, "X1"), # red, yellow
    Butt(8, 7, 11, "High Score"), # white, green
    Butt(18, 23, 12, "C") # black, blue
]

SOLENOID = OutputDevice(14)
RED_LED = LED(2)
REED = DigitalInputDevice(4)

##################
# Flash Patterns #
##################
def flash(buttons,time,count):
    logging.debug("Flash all buttons")
    i=0
    while i < count: 
        for b in buttons:
            b.led.on()
        sleep (time)

        for b in buttons:
            b.led.off()
        sleep (time)
        i+=1

def count_leds(buttons,time,direction):
    logging.debug("Count Down LED")
    for b in buttons:
        if direction=="up":
            sleep(time)
        b.led.on()

    sleep(time*3)

    for b in buttons:
        if direction == "down":
            sleep (time)
        b.led.off()

def fanfare(buttons,delay):
    # All light up, 
    for b in buttons:
        b.led.on()
    
    # turn off in sequence
    for b in buttons:
        sleep(delay)
        b.led.off()
    sleep(delay)

def sparkle(buttons,delay,duration):
    logging.debug("Sparkle")
    i=0
    while i < duration:
        active_butt = buttons[random.randint(0,len(buttons)-1)]
        active_butt.led.on()
        sleep(delay)
        active_butt.led.off()
        i+=1

def bounce_rows(buttons,duration,count):
    logging.debug("Bounce Rows")
    rows = [
        [10,11,0],
        [9,1],
        [8,2],
        [7,3],
        [4,5,6]
    ]
    bounce_rows_cols(buttons,rows,duration,count)

def bounce_cols(buttons,duration,count):
    logging.debug("Bounce Cols")
    cols = [
        [10,8,6],
        [7,9],
        [5,11],
        [1,3],
        [0,2,4]
    ]
    bounce_rows_cols(buttons,cols,duration,count)


def bounce_rows_cols(buttons,rows_cols,duration,count):

    row_col_on(rows_cols[0])
    sleep(duration)      
    j=0
    while j<count:
        i = 1
        while i < len(rows_cols):
            row_col_off(rows_cols[i-1])
            row_col_on(rows_cols[i])
            sleep(duration)
            i+=1
        
        i = len(rows_cols)-1
        while i > 0:
            row_col_off(rows_cols[i])
            row_col_on(rows_cols[i-1])
            sleep(duration)
            i-=1
        
        j+=1

    sleep(duration)
    row_col_off(rows_cols[0])

def row_col_on(arr):
    for id in arr:
        buttons[id].led.on()

def row_col_off(arr):
    for id in arr:
        buttons[id].led.off()

def circle(buttons,duration,count):
    logging.debug("Circle LED's")
    
    groups = [
        [0,1],
        [2],
        [3,4],
        [5],
        [6,7],
        [8],
        [9,10],
        [11]
    ]
    # start with 12 O'Clock on
    buttons[11].led.on()
    sleep(duration)
    buttons[11].led.off()
    i=0
    while i<count:
        for group in groups:
            for b in group:
                buttons[b].led.on()
            sleep(duration)
            for b in group:
                buttons[b].led.off()
        i+=1

def roman_score(buttons,score):
    logging.debug("Calculate Roman Score")
    
    rom_score = score
    verbal_rom_score = ""
    rosetta = [
        [11,100],
        [0,50],
        [9,10],
        [1,10],
        [8,10],
        [2,10],
        [7,5],
        [3,1],
        [6,1],
        [5,1],
        [4,1]
    ]

    for ros in rosetta:
        if rom_score >= ros[1]:
            buttons[ros[0]].led.on()
            rom_score = rom_score - ros[1]
            verbal_rom_score=verbal_rom_score+buttons[ros[0]].roman
    
    logging.info("Score: {}. Roman Score: {}".format(score, verbal_rom_score))

    high_score = int(config.get('HighScore','high_score'))
    
    if score > high_score:
        logging.info("New High Score, writing high_score={} to config".format(score))
        buttons[10].led.on()
        # write new highscore into config
        config['HighScore'] = {'high_score':score}
        with open(config_loc, 'w') as configfile:
            config.write(configfile)
        configfile.close
    
    sleep(6)
    for b in buttons:
        b.led.off()

##############
# Operations #
##############

def open_solenoid():
    logging.debug("Opening Solenoid")
    SOLENOID.on()
    sleep(20)
    logging.info("Closing Solenoid")
    SOLENOID.off()

def play():
    # Run game startup
    logging.info("Game Started")
    #fanfare(buttons,0.2)
    # Flash Once
    #flash(buttons,0.2,1)

    count_leds(buttons,0.4,"up")

    start_time = time.time()
    end_time = start_time + game_duration
    
    score=0
    while time.time() < end_time:
        active_b = random.randint(0,len(buttons)-1)
        logging.debug("button array int is {}".format(active_b))
        logging.debug("Button selected is Button {}. Turn on {} LED".format(buttons[active_b].id,buttons[active_b].id))
        buttons[active_b].led.on()
        logging.debug("Awaiting Button Press")
        buttons[active_b].button.wait_for_press()
        logging.debug("Buton pressed")
        buttons[active_b].led.off()
        sleep(0.2)
        score+=1
    
    flash(buttons,1,1)
    
    logging.info("Game ran for {} seconds".format(time.time()-start_time))
    logging.info("Game Over: Score = {}".format(score))

    # If high enough score 
    if score >= winning_score:
        # sparkle random lights end in big flash
        sparkle(buttons,0.025,160)
        # Open solenoid 10 sec
        logging.info("We have a winner!")
        x = threading.Thread(target = open_solenoid)
        x.start()
    else:
        # else 3 flash quick succession
        flash(buttons,0.1,3)
        RED_LED.blink(0.2,0.2,5,True)
    sleep(0.8)
    roman_score(buttons,score)

def display_high_score():
    high_score = int(config.get('HighScore','high_score'))
    roman_score(buttons,high_score)

def backdoor():
    logging.info("Checking Backdoor")
    for b in buttons:
        logging.debug("Button {} is held: {}".format(b.id,b.button.is_held))

    # backdoor not open if 
    if buttons[1].button.is_held & buttons[5].button.is_held:
        for i in range(2,12):
            if buttons[i].button.is_held:
                if  i!=5:
                    logging.info("Backdoor not open")
                    sleep(1)
                    return
        
        logging.info("Backdoor opened, opening solenoid")
        sleep(2)
    else:
        logging.info("Backdoor definitely not open")
        sleep(1)

if __name__ == '__main__':

    logging.info("Red LED")
    RED_LED.blink(1,1,2,True)
    bounce_cols(buttons,0.1,3)
    sleep(0.2)
    bounce_rows(buttons,0.1,3)
    sleep(0.2)
    circle(buttons, 0.15,3)
    sleep(0.2)
    sparkle(buttons,0.05,40)
    sparkle(buttons,0.025,80)
    

    # Start wait on magnetic sensor
    
    # TODO change to when_active
    # tried when_active but when i do that - the button presses aren't registered...
    
    # Same goes for these functtions
    #buttons[10].button.when_held=display_high_score
    #buttons[0].button.when_held=backdoor

    i=0
    while True:
        if REED.is_active:
            logging.debug("Start Game")
            play()
        elif buttons[10].button.is_held:
            display_high_score()
        elif buttons[0].button.is_held:
            backdoor()
        else:
            if i % 40 == 0:
                logging.debug("wait for game to start")
            i+=1
            sleep(0.25)
    
    pause()
