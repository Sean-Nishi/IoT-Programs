#Sean Nishi
#Assignment 4

from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import datetime
import time

#set up a client for influxdb
dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')

#set up pi pin for the light
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

#broker_address = "10.0.0.67"
broker_address = "192.168.1.12"

LIGHT_THRESHOLD = 500;

################################################################
#when we receive a message from the arduino
def on_message(client, userdata, message):
    temp = float(message.payload.decode())
    print(temp)
    #save the value to the database
    #setup json data struct
    json_body = [
        {
            "measurement": '/light',
            "time": datetime.datetime.utcnow(),
            "fields": {
                "value": temp
            }
        }
    ]

    #write to db
    dbclient.write_points(json_body)
################################################################    

#set up mqtt server
client = mqtt.Client()
client.connect(broker_address)
client.on_message=on_message
client.subscribe("/light")

#database query
query = 'select mean("value") from "/light" where "time" > now() - 10s'

client.loop_start()

while True:
    print("tick")
    #query the database
    result = dbclient.query(query)
    
    try:
        #bug trying to get a list of all the resulting points
        mean = list(result.get_points(measurement='/light'))[0]['mean']
        
        #get the average light after saving to database
        if(mean <= LIGHT_THRESHOLD):  
            #turn led on
            print("turning light on")
            GPIO.output(21, 1)
        else:
            #turn led off
            print("turning light off")
            GPIO.output(21, 0)
    except:
        print("Exception")
        pass

    #wait 10 seconds before querying
    time.sleep(10)

client.loop_stop()
