#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>
#include <MQUnifiedsensor.h>
MQUnifiedsensor MQ7("ESP-32", 3.3, 12, 32, "MQ-7");
float COppm;

const char *ssid = "ssid";
const char *password = "password";

WebSocketsClient websocket;

WiFiClient client;

char path[] = "/ws/device/temp/";

char host[] = "192.168.1.14";

const uint16_t port = 8000;

StaticJsonDocument<100> doc;
StaticJsonDocument<100> doc2;

#define DEBUG_SERIAL Serial

// 宣告讀取溫溼度的變數
String jsonString;
String jsonString1;
int interval = 5000;
unsigned long previousMillis = 0;

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

void sendData()
{
  JsonObject root = doc.to<JsonObject>();
  JsonObject root1 = doc2.to<JsonObject>();
  if (digitalRead(LED_BUILTIN) == HIGH)
  {
    MQ7.update();             // Update data, the arduino will be read the voltage on the analog pin
    COppm = MQ7.readSensor(); // Sensor will read PPM concentration using the model and a and b values setted before or in the setup
    doc2["COppm"] = COppm;
    doc2["device_type"] = "MQ7";
    serializeJson(doc2, jsonString1);
    doc["message"] = jsonString1;
    serializeJson(doc, jsonString);
    DEBUG_SERIAL.println(jsonString);
    DEBUG_SERIAL.println(doc["message"].as<String>().c_str());
    websocket.sendTXT(jsonString);
    jsonString = "";
    jsonString1 = "";
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

  MQ7.setRegressionMethod(1); //_PPM =  a*ratio^b
  MQ7.setA(99.042);
  MQ7.setB(-1.518); // Configurate the ecuation values to get CO concentration
  MQ7.init();

  Serial.print("Calibrating please wait.");
  float calcR0 = 0;
  for (int i = 1; i <= 10; i++)
  {
    MQ7.update(); // Update data, the arduino will be read the voltage on the analog pin
    calcR0 += MQ7.calibrate(27.5);
    Serial.print(".");
  }
  MQ7.setR0(calcR0 / 10);
  Serial.println("  done!.");
  if (isinf(calcR0))
  {
    Serial.println("Warning: Conection issue founded, R0 is infite (Open circuit detected) please check your wiring and supply");
    while (1)
      ;
  }
  if (calcR0 == 0)
  {
    Serial.println("Warning: Conection issue founded, R0 is zero (Analog pin with short circuit to ground) please check your wiring and supply");
    while (1)
      ;
  }
  MQ7.serialDebug(true);

  pinMode(LED_BUILTIN, OUTPUT);
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