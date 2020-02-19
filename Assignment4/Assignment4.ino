//Sean Nishi
//Assignment 4

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <String.h>

//WiFi/MQTT parameters
#define WLAN_SSID       "dan_2"
#define WLAN_PASS       "supersecretpassword"
#define BROKER_IP       "192.168.1.12"

//refresh interval in ms
static const unsigned long REFRESH_INTERVAL = 1000;
static unsigned long lastRefreshTime = 0;

//wifi and mqtt stuff
WiFiClient client;
PubSubClient mqttclient(client);

int lightstate;
char buffer [6];

void setup() {
  Serial.begin(115200);

  //setup wifi
  WiFi.mode(WIFI_STA);
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }

  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  //connect to mqtt server
  mqttclient.setServer(BROKER_IP, 1883);
  connect();

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
    lightstate = analogRead(A0);

    //publish info to broker/pi
    mqttclient.publish("/light", itoa(lightstate, buffer, 10));
    Serial.println(itoa(lightstate, buffer, 10));
  }

  //ticks every loop
  Serial.println("tick");
  delay(1000);
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
