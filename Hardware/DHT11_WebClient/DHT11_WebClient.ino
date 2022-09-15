#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

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

//宣告DHT11資料讀取物件
#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// 宣告讀取溫溼度的變數
String jsonString;
String jsonString1;
float temperature;
float humidity;
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
        temperature = dht.readTemperature();
        humidity = dht.readHumidity();
        doc2["temperature"] = temperature;
        doc2["humidity"] = humidity;
        doc2["device_type"] = "DHT11";
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
    dht.begin();
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
