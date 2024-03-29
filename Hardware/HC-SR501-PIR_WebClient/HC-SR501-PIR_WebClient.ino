#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>

const char *ssid = "ssid";
const char *password = "password";

WebSocketsClient websocket;

WiFiClient client;

char path[] = "/ws/chat/temp/";

char host[] = "192.168.100.2";

const uint16_t port = 8000;

StaticJsonDocument<100> doc;

#define DEBUG_SERIAL Serial

String jsonString;
int interval = 5000;
unsigned long previousMillis = 0;

int sensor = 4;
int val = 0;

void sendData()
{
  JsonObject root = doc.to<JsonObject>();
  val = digitalRead(sensor); // read sensor value
  if (val == HIGH)
  {

    DEBUG_SERIAL.println("Motion detected!");
    doc["message"] = "Motion detected!";
  }
  else
  {
    DEBUG_SERIAL.println("Motion stopped!");
    doc["message"] = "Motion stopped!";
  }
  serializeJson(doc, jsonString);
  DEBUG_SERIAL.println(jsonString);
  websocket.sendTXT(jsonString);
  jsonString = "";
}
void webSocketEvent(WStype_t type, uint8_t *payload, size_t length)
{

  switch (type)
  {
  case WStype_DISCONNECTED:
    DEBUG_SERIAL.printf("[WSc] Disconnected!\n");
    digitalWrite(LED_BUILTIN, LOW);
    break;
  case WStype_CONNECTED:
    DEBUG_SERIAL.printf("[WSc] Connected to url: %s\n", payload);
    digitalWrite(LED_BUILTIN, HIGH);
    // send message to server when Connected
    // webSocketClient.sendTXT("Connected");
    break;
  case WStype_TEXT:
    if (deserializeJson(doc, payload))
    {
      DEBUG_SERIAL.printf("[WSc] DeserializeJson() failed: %s\n", deserializeJson(doc, payload).c_str());
      return;
    }
    DEBUG_SERIAL.printf("[WSc] get text: %s\n", doc["message"].as<String>().c_str());
    if (doc["message"] == "on")
    {
      digitalWrite(LED_BUILTIN, HIGH);
    }
    else if (doc["message"] == "off")
    {
      digitalWrite(LED_BUILTIN, LOW);
    }
    // send message to server
    // webSocketClient.sendTXT("message here");
    break;
  }
}

void setup()
{
  DEBUG_SERIAL.begin(115200);
  DEBUG_SERIAL.setDebugOutput(true);
  delay(1000);

  // We start by connecting to a WiFi network
  WiFi.begin(ssid, password);

  DEBUG_SERIAL.println();
  DEBUG_SERIAL.println();
  DEBUG_SERIAL.println("Waiting for WiFi... ");

  while (WiFi.status() != WL_CONNECTED)
  {
    DEBUG_SERIAL.print(".");
    delay(500);
  }

  DEBUG_SERIAL.println("");
  DEBUG_SERIAL.println("WiFi connected");
  DEBUG_SERIAL.print("IP address: ");
  DEBUG_SERIAL.println(WiFi.localIP());

  delay(3000);

  websocket.begin(host, port, path);
  // webSocketClient.beginSSL(host, 443, path);
  websocket.onEvent(webSocketEvent);
  websocket.setReconnectInterval(5000);

  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(sensor, INPUT);
}

void loop()
{
  websocket.loop();
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval)
  {
    sendData();
    previousMillis = currentMillis;
  }
}
