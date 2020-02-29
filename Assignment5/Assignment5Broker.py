#Sean Nishi
#Assignment 5

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from influxdb import InfluxDBClient
import datetime

broker_address= "172.17.0.1"

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

#######################################################
def on_message(client, userdata, message):
    print(message.topic + " " + str(message.payload))

    #switching lights on/off from messages
    if(message.topic == '/device/pi'):
        print("got message to turn on/off led")
        
        if(message.payload.decode() == 'on'):
            print("turning pi light on")
            GPIO.output(23, 1)
            print("done")
            
        elif(message.payload.decode() == 'off'):
            print("turning pi light off")
            GPIO.output(23, 0)
            print("done")
    
    #write new light value to db
    if(message.topic == '/light_level'):
        json_body = [
            {
                "measurement": '/light_level',
                "time": datetime.datetime.utcnow(),
                "fields": {
                    "value": float(message.payload.decode())
                }
            }
        ]
        
        dbclient.write_points(json_body)
#######################################################
client = mqtt.Client()
client.connect(broker_address)

client.on_message=on_message

client.subscribe("/light_level")
client.subscribe("/device/pi")

dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')

client.loop_start()

try:
    while True:
        pass
except KeyboardInterrupt:
    pass

client.loop_stop()
GPIO.cleanup()
