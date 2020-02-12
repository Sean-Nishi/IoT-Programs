//Sean Nishi
//Assignment 3
//program creates a mqtt client that both publishes and subscribes to to the broker

//in loop(), need to check for button press on arduino. if detected, then send message to
//pi to turn on the light

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <String.h>

//WiFi/MQTT parameters
#define WLAN_SSID       "dan_2"
#define WLAN_PASS       "supersecretpassword"
#define BROKER_IP       "192.168.1.12"

//input and output setup
#define BUTTON D2
#define LED D1

bool buttonState = LOW;
bool clickedFlag = LOW;
bool light = LOW;

bool onoff = LOW;

WiFiClient client;
PubSubClient mqttclient(client);

//when message is received from broker, do stuff
void callback (char* topic, byte* payload, unsigned int length){
  //set the payload received into a string and null terminate
  payload[length] = '\0'; // add null terminator to byte payload so we can treat it as a string

  if (strcmp(topic, "/led/arduino") == 0){
     if (strcmp((char *)payload, "on") == 0){
        digitalWrite(LED, HIGH);
     } else if (strcmp((char *)payload, "off") == 0){
        digitalWrite(LED, LOW);
     }
  }
}

void setup() {
  Serial.begin(115200);

  //connect to wifi
  WiFi.mode(WIFI_STA);
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }

  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  //create a mqtt server
  mqttclient.setServer(BROKER_IP, 1883);
  mqttclient.setCallback(callback);
  connect();

  //connect client to mqtt server
  mqttclient.setServer(BROKER_IP, 1883);
  connect();

  pinMode(LED, OUTPUT);
  pinMode(BUTTON, INPUT);
}

void loop() {
  //check for disconnect
  if (!mqttclient.connected()){
    connect();
  }
  mqttclient.loop();

  buttonState = digitalRead(BUTTON);

  if (buttonState and not clickedFlag){
    clickedFlag = HIGH;
  }

  if (not buttonState and clickedFlag){
    clickedFlag = LOW;
    
    if (light == LOW){
      Serial.print("Publishing \"on\" to /led/pi\n");
      mqttclient.publish("/led/pi", "on");
      light = HIGH;
    }
    else if (light == HIGH){
      Serial.print("Publishing \"off\" to /led/pi\n");
      mqttclient.publish("/led/pi", "off");
      light = LOW;
    }
  }
}

//make sure publisher is connected to the wifi and the broker
void connect(){
  //make sure we are connected to the wifi
  while (WiFi.status() != WL_CONNECTED){
    Serial.println("Wifi issue");
    delay(3000);
  }

  Serial.print("Connecting to MQTT server... ");

  while(!mqttclient.connected()){
    //we are connected to the broker, subscribe to a topic
    if (mqttclient.connect(WiFi.macAddress().c_str())){
      Serial.println("MQTT server Connected!");
      //subscribe to the topic
      mqttclient.subscribe("/led/arduino");
    }
    //we havent connected to the broker, wait and try again
    else {
      Serial.print(F("MQTT server connection failed! rc="));
      Serial.print(mqttclient.state());
      Serial.println("try again in 5 seconds");
      delay(20000);
    }
  }
}
