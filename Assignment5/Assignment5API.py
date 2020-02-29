#Sean Nishi
#Assignment 5

from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
import datetime
from flask import Flask, request, json
from flask_restful import Resource, Api
import string

broker_address = "172.17.0.1"

LIGHT_THRESHOLD = 700

client = mqtt.Client()
client.connect(broker_address)

dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')

#database query
query = 'select mean("value") from "/light_level" where "time" > now() - 10s'

app = Flask(__name__)
api = Api(app)

###################################################################
class LightStuff(Resource):
    #get mean light level, return the value
    def get(self):
        try:
            result = dbclient.query(query)
            print("returning mean")
            mean = list(result.get_points(measurement='/light_level'))[0]['mean']
            return mean
        except:
            print("exception getting average data")

    #post to esp and broker, didnt return anything, will print null
    def post(self):
        value = request.get_data()
        value = json.loads(value)
        print(value)

        #check which device
        if (value["device"] == "pi"):
            #check led state...
            if(value["state"] == "on"):
                print("publishing pi led on")
                client.publish("/device/pi", "on")
                print("done")

            elif(value["state"] == "off"):
                print("publishing pi led off")
                client.publish("/device/pi", "off")
                print("done")

        elif(value["device"] == "arduino"):
            #check led state
            if(value["state"] == "on"):
                print("publishing arduino led on")
                client.publish("/device/arduino", "on")
                print("done")

            elif(value["state"] == "off"):
                print("publishing arduino led off")
                client.publish("/device/arduino", "off")
                print("done")
                
####################################################################

api.add_resource(LightStuff, '/light')

app.run(host = '0.0.0.0', debug = True)
