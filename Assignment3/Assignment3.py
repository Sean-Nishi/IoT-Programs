#Sean Nishi
#Assignment 3

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

#ip address
broker_address = "192.168.1.12"

#set up pi pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)
GPIO.setup(6, GPIO.OUT)

# when client receives message from broker, respond accordingly
def on_message(client, userdata, message):
    if (message.payload.decode() == "on"):
        print("MESSAGE RECEIVED: turning on\n")
        GPIO.output(6, 1)
    elif (message.payload.decode() == "off"):
        print("MESSAGE RECEIVED: turning off\n")
        GPIO.output(6, 0)



#create client and connect to broker
client = mqtt.Client()
client.connect(broker_address)
client.on_message=on_message

#temp vars
buttonState = False
clicked = False
led = False

#have the client subscribe to the pi folder
client.subscribe("/led/pi")

#start the client
client.loop_start()

#run until keyboard interrupt
try:
    while True:
        #sending stuff to arduino
        buttonState = GPIO.input(21)
        #if the button has been pressed
        #send message to broker
        if (buttonState and not clicked):
            clicked = True
            
        if (not buttonState and clicked):
            clicked = False
            #respond accordingly
            if (led == True):
                client.publish("/led/arduino", "off")
                led = False
            elif (led == False):
                client.publish("/led/arduino", "on")
                led = True

        pass

except KeyboardInterrupt:
    pass

client.loop_stop()
