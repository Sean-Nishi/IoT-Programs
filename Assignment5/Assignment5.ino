//Sean Nishi
//Assignment 5

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <String.h>

//WiFi/MQTT params
#define WLAN_SSID       "Eldritch_Moon"
#define WLAN_PASS       "got_420_logicool_grapes"
#define BROKER_IP       "10.0.0.67"

#define LED D1
#define SENSOR A0

WiFiClient client;
PubSubClient mqttclient(client);

//refresh interval in ms
static const unsigned long REFRESH_INTERVAL = 1000;
static unsigned long lastRefreshTime = 0;
const int LIGHT_THRESHOLD = 500;

int lightstate;
char buffer [6];

//when message is received from broker, do stuff
void callback (char* topic, byte* payload, unsigned int length){
  //set the payload received into a string and null terminate
  payload[length] = '\0'; // add null terminator to byte payload so we can treat it as a string

  if (strcmp(topic, "/device/arduino") == 0){
     if (strcmp((char *)payload, "on") == 0){
        Serial.println("turning ard led on");
        digitalWrite(LED, HIGH);
     } else if (strcmp((char *)payload, "off") == 0){
        Serial.println("turning ard led off");
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

  pinMode(LED, OUTPUT);
  pinMode(SENSOR, INPUT);
}

void loop() {
  //mqtt server stuff
  if(!mqttclient.connected()){
    connect();
  }
  mqttclient.loop();

  
  //runs every 1 second
  if(millis() - lastRefreshTime >= REFRESH_INTERVAL){
    lastRefreshTime += REFRESH_INTERVAL;
    lightstate = analogRead(SENSOR);

    //publish light level info to broker/pi
    mqttclient.publish("/light_level", itoa(lightstate, buffer, 10));
    Serial.println(itoa(lightstate, buffer, 10));
  }
  
  
  
  //ticks every loop
  Serial.println("tick");
  delay(3000);
}

//make sure mqtt client is connected to the wifi and the broker
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
        //subscribe to arduino device
        mqttclient.subscribe("/device/arduino");
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
