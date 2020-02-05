#Sean Nishi
#Assignment 2

import RPi.GPIO as GPIO

#set up board
GPIO.setmode(GPIO.BCM)

#set up pins
GPIO.setup(21, GPIO.IN)

GPIO.setup(18, GPIO.OUT)

buttonState = False
led = False
changed = False

while True:
    #is the button pressed?
    buttonState = GPIO.input(21)

    #if button is pressed, have we already changed the light?
    if buttonState == False:
        changed = False

    #if we havent change the light
    if (changed == False and buttonState == True):
        #and if the button is pressed and the light is on
        #set light to on and save the state
        if (led == True):
            GPIO.output(18, GPIO.LOW)
            led = False
            changed = True

        #else if the button is pressed and the light is off
        #turn the light on and save the state
        elif (led == False):
            GPIO.output(18, GPIO.HIGH)
            led = True
            changed = True
