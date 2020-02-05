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
clicked = False

while True:
    #is the button pressed?
    buttonState = GPIO.input(21)

    #if the button is clicked and it wasn't previously clicked
    if (buttonState and not clicked):
        clicked = True

    #if we havent change the light
    if (not buttonState and clicked):
        clicked = False
        
        #and if the button is pressed and the light is on
        #set light to on and save the state
        if (led == True):
            GPIO.output(18, GPIO.LOW)
            led = False

        #else if the button is pressed and the light is off
        #turn the light on and save the state
        elif (led == False):
            GPIO.output(18, GPIO.HIGH)
            led = True
