#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>
#include "PinDefinitionsAndMore.h" // Define macros for input and output pin etc.
#include <IRremote.hpp>

const char *ssid = "113";
const char *password = "77777777";

WebSocketsClient websocket;

WiFiClient client;

char path[] = "/ws/chat/ir/";

char host[] = "api.bap5.cc";

const uint16_t port = 8000;

StaticJsonDocument<100> doc;

#define DEBUG_SERIAL Serial

// 宣告變數
String jsonString;
int interval = 60000;
unsigned long previousMillis = 0;
const uint16_t rawData_power[67] = {9980, 4420, 630, 620, 580, 620, 580, 670, 580, 570, 630, 620, 580, 620, 580, 670, 580, 1670, 630, 1670, 630, 1670, 630, 1670, 630, 1720, 580, 1770, 580, 1720, 580, 1720, 580, 620, 580, 620, 630, 1720, 580, 620, 580, 620, 630, 1720, 580, 620, 580, 620, 630, 620, 580, 1720, 580, 620, 580, 1720, 630, 1670, 630, 620, 580, 1770, 530, 1770, 580, 1670, 630}; // Protocol=NEC Address=0x80 Command=0x12 Raw-Data=0xED127F80 32 bits LSB first

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
    if (doc["message"] == "power")
    {
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println(F("Send Raw Data(16 bit array format)"));
      // Serial.flush();

      IrSender.sendRaw(rawData_power, sizeof(rawData_power) / sizeof(rawData_power[0]), NEC_KHZ);
    }
    else if (doc["message"] == "light")
    {
      /* code */
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println(F("Send Raw Data(16 bit array format)"));
      Serial.flush();

      uint16_t rawData[67] = {10030, 4520, 580, 620, 630, 620, 580, 620, 630, 620, 630, 570, 630, 620, 630, 570, 630, 1720, 580, 1720, 630, 1670, 630, 1720, 630, 1670, 630, 1670, 680, 1670, 630, 1670, 630, 620, 630, 570, 680, 1620, 680, 1670, 630, 1670, 630, 1670, 680, 520, 680, 570, 630, 570, 680, 1620, 680, 570, 630, 570, 630, 570, 630, 570, 630, 1720, 630, 1670, 630, 1670, 630}; // Protocol=NEC Address=0x80 Command=0x1E Raw-Data=0xE11E7F80 32 bits LSB first

      IrSender.sendRaw(rawData, sizeof(rawData) / sizeof(rawData[0]), NEC_KHZ);
    }

    else if (doc["message"] == "sp_up")
    {
      /* code */
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println(F("Send Raw Data(16 bit array format)"));
      Serial.flush();

      uint16_t rawData[67] = {10080, 4420, 680, 570, 630, 570, 630, 620, 630, 570, 630, 570, 680, 570, 630, 570, 630, 1670, 630, 1670, 680, 1620, 630, 1720, 630, 1670, 630, 1670, 630, 1720, 630, 1670, 630, 620, 680, 1670, 630, 570, 680, 570, 680, 1670, 630, 570, 680, 570, 630, 620, 630, 570, 680, 570, 630, 1670, 630, 1720, 630, 570, 680, 1670, 630, 1670, 630, 1670, 630, 1720, 630}; // Protocol=NEC Address=0x80 Command=0x9 Raw-Data=0xF6097F80 32 bits LSB first

      IrSender.sendRaw(rawData, sizeof(rawData) / sizeof(rawData[0]), NEC_KHZ);
    }

    else if (doc["message"] == "sp_dw")

    {
      /* code */
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println(F("Send Raw Data(16 bit array format)"));
      Serial.flush();

      uint16_t rawData[67] = {10080, 4470, 580, 670, 580, 620, 580, 670, 580, 620, 580, 670, 580, 570, 630, 620, 630, 1670, 630, 1670, 630, 1670, 630, 1720, 580, 1720, 580, 1720, 630, 1670, 630, 1720, 580, 620, 630, 1670, 630, 1720, 630, 1670, 630, 1670, 630, 1720, 580, 620, 630, 620, 580, 620, 580, 620, 630, 570, 630, 620, 580, 620, 630, 620, 580, 1720, 630, 1670, 580, 1720, 630}; // Protocol=NEC Address=0x80 Command=0x1F Raw-Data=0xE01F7F80 32 bits LSB first

      IrSender.sendRaw(rawData, sizeof(rawData) / sizeof(rawData[0]), NEC_KHZ);
    }
    break;
  }
}

void sendData()
{
  JsonObject root = doc.to<JsonObject>();

  doc["message"] = "";
  serializeJson(doc, jsonString);
  DEBUG_SERIAL.println(doc["message"].as<String>().c_str());
  websocket.sendTXT(jsonString);
  jsonString = "";
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

  // websocket.begin(host, port, path);
  websocket.beginSSL(host, 443, path);
  websocket.onEvent(webSocketEvent);

  websocket.setReconnectInterval(5000);

  pinMode(LED_BUILTIN, OUTPUT);

#if defined(__AVR_ATmega32U4__) || defined(SERIAL_PORT_USBVIRTUAL) || defined(SERIAL_USB) /*stm32duino*/ || defined(USBCON) /*STM32_stm32*/ || defined(SERIALUSB_PID) || defined(ARDUINO_attiny3217)
  delay(4000); // To be able to connect Serial monitor after reset or power up and before first print out. Do not wait for an attached Serial Monitor!
#endif
  // Just to know which program is running on my Arduino
  Serial.println(F("START " __FILE__ " from " __DATE__ "\r\nUsing library version " VERSION_IRREMOTE));

#if defined(IR_SEND_PIN)
  IrSender.begin(); // Start with IR_SEND_PIN as send pin and enable feedback LED at default feedback LED pin
#else
  IrSender.begin(4, ENABLE_LED_FEEDBACK); // Specify send pin and enable feedback LED at default feedback LED pin
#endif
  Serial.println(F("Ready to send IR signals at pin " STR(IR_SEND_PIN)));
}

void loop()
{
  websocket.loop();
}