#include <Arduino.h>
#include <WiFi.h>
#include "EEPROM.h"
#include "HTTPClient.h"
#include <WiFiClientSecure.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>
#include <IRremote.hpp>
#define LENGTH(x) (strlen(x) + 1) // length of char string
#define EEPROM_SIZE 200           // EEPROM size
#define WiFi_rst 0
#define DEBUG_SERIAL Serial

String ssid; // string variable to store ssid
String pss;  // string variable to store password
String customData;
char *aes = "McQfTjWnZr4u7x!A"; // AES key
unsigned long rst_millis;

HTTPClient http;
WebSocketsClient websocket;

WiFiClient client;

char path[] = "/ws/chat/ir/";
char host[] = "api.bap5.cc";
String request = "https://api.bap5.cc/auth/device_data/";

const uint16_t port = 8000;

StaticJsonDocument<200> doc;
StaticJsonDocument<200> doc1;
StaticJsonDocument<200> doc2;
StaticJsonDocument<200> doc3;

// 宣告讀取溫溼度的變數
String jsonString;
String jsonString1;
String jsonString2;
String jsonString3;
float temperature;
float humidity;
int interval = 5000;
unsigned long previousMillis = 0;

void WiFiEvent(WiFiEvent_t event, WiFiEventInfo_t info)
{
  Serial.printf("[WiFi-event] event: %d\n", event);

  switch (event)
  {

  case ARDUINO_EVENT_SC_GOT_SSID_PSWD:
  {
    DEBUG_SERIAL.println("Got SSID and password");

    uint8_t ssid[33] = {0};
    uint8_t password[65] = {0};

    uint8_t rvd_data[64] = {0};

    memcpy(ssid, info.sc_got_ssid_pswd.ssid, sizeof(info.sc_got_ssid_pswd.ssid));
    memcpy(password, info.sc_got_ssid_pswd.password, sizeof(info.sc_got_ssid_pswd.password));

    DEBUG_SERIAL.printf("SSID:%s\n", ssid);
    DEBUG_SERIAL.printf("PASSWORD:%s\n", password);

    if (info.sc_got_ssid_pswd.type == SC_TYPE_ESPTOUCH_V2)
    {
      ESP_ERROR_CHECK(esp_smartconfig_get_rvd_data(rvd_data, sizeof(rvd_data)));

      customData = (char *)rvd_data;

      DEBUG_SERIAL.printf("RVD_DATA:%s\n", customData.c_str());
      // DEBUG_SERIAL.println("RVD_DATA");
      // DEBUG_SERIAL.write(rvd_data, 64);
      // DEBUG_SERIAL.printf("\n");
    }
  }
  break;
  }
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
    if (doc["message"] == "power")
    {
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println(F("Send Raw Data(16 bit array format)"));
      Serial.flush();

      uint16_t rawData[67] = {9980, 4420, 630, 620, 580, 620, 580, 670, 580, 570, 630, 620, 580, 620, 580, 670, 580, 1670, 630, 1670, 630, 1670, 630, 1670, 630, 1720, 580, 1770, 580, 1720, 580, 1720, 580, 620, 580, 620, 630, 1720, 580, 620, 580, 620, 630, 1720, 580, 620, 580, 620, 630, 620, 580, 1720, 580, 620, 580, 1720, 630, 1670, 630, 620, 580, 1770, 530, 1770, 580, 1670, 630}; // Protocol=NEC Address=0x80 Command=0x12 Raw-Data=0xED127F80 32 bits LSB first

      IrSender.sendRaw(rawData, sizeof(rawData) / sizeof(rawData[0]), NEC_KHZ);
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
  if (digitalRead(LED_BUILTIN) == HIGH)
  {
    JsonObject root = doc.to<JsonObject>();
    doc["message"] = "";
    serializeJson(doc, jsonString);
    DEBUG_SERIAL.println(doc["message"].as<String>().c_str());
    websocket.sendTXT(jsonString);
    jsonString = "";
  }
}

void sendRestful()
{
}

void setup()
{

  DEBUG_SERIAL.begin(115200);
  DEBUG_SERIAL.setDebugOutput(true);
  delay(1000);                    // Init serial
  pinMode(LED_BUILTIN, OUTPUT);   // Init LED
  digitalWrite(LED_BUILTIN, LOW); // Turn off LED
  pinMode(WiFi_rst, INPUT);
  if (!EEPROM.begin(EEPROM_SIZE))
  { // Init EEPROM
    DEBUG_SERIAL.println("failed to init EEPROM");
    delay(1000);
  }
  else
  {
    ssid = readStringFromFlash(0); // Read SSID stored at address 0
    DEBUG_SERIAL.printf("SSID = %s\n", ssid);
    pss = readStringFromFlash(40); // Read Password stored at address 40
    DEBUG_SERIAL.printf("psss = %s\n", pss);
    customData = readStringFromFlash(60); // Read custom data stored at address 60
    DEBUG_SERIAL.printf("Custom data = %s\n", customData);
  }

  WiFi.begin(ssid.c_str(), pss.c_str());

  delay(3500); // Wait for a while till ESP connects to WiFi

  if (WiFi.status() != WL_CONNECTED) // if WiFi is not connected
  {
    // Init WiFi as Station, start SmartConfig
    WiFi.mode(WIFI_AP_STA);
    WiFi.onEvent(WiFiEvent);
    WiFi.beginSmartConfig(SC_TYPE_ESPTOUCH_V2, aes);

    // Wait for SmartConfig packet from mobile
    DEBUG_SERIAL.println("Waiting for SmartConfig.");
    while (!WiFi.smartConfigDone())
    {
      delay(500);
      DEBUG_SERIAL.print(".");
    }

    DEBUG_SERIAL.println("");
    DEBUG_SERIAL.println("SmartConfig received.");

    // Wait for WiFi to connect to AP
    DEBUG_SERIAL.println("Waiting for WiFi");
    while (WiFi.status() != WL_CONNECTED)
    {
      delay(500);
      DEBUG_SERIAL.print(".");
    }
    digitalWrite(LED_BUILTIN, HIGH); // Turn on LED
    DEBUG_SERIAL.println("WiFi Connected.");

    DEBUG_SERIAL.print("IP Address: ");
    DEBUG_SERIAL.println(WiFi.localIP());

    // read the connected WiFi SSID and password
    ssid = WiFi.SSID();
    pss = WiFi.psk();
    DEBUG_SERIAL.print("SSID:");
    DEBUG_SERIAL.println(ssid);
    DEBUG_SERIAL.print("PSS:");
    DEBUG_SERIAL.println(pss);
    DEBUG_SERIAL.println("Store SSID & PSS in Flash");
    writeStringToFlash(ssid.c_str(), 0);        // storing ssid at address 0
    writeStringToFlash(pss.c_str(), 40);        // storing pss at address 40
    writeStringToFlash(customData.c_str(), 60); // storing pss at address 40
  }
  else
  {
    DEBUG_SERIAL.println("WiFi Connected");
  }

  delay(3000);
  http.addHeader("Content-Type", "application/json");
  http.begin(request);

  // websocket.begin(host, port, path);
  websocket.beginSSL(host, 443, path);
  websocket.onEvent(webSocketEvent);
  websocket.setReconnectInterval(5000);
}

void loop()
{
  websocket.loop();
  // put your main code here, to run repeatedly:
  rst_millis = millis();
  while (digitalRead(WiFi_rst) == LOW)
  {
    // Wait till boot button is pressed
  }
  // check the button press time if it is greater than 3sec clear wifi cred and restart ESP
  if (millis() - rst_millis >= 3000)
  {
    DEBUG_SERIAL.println("Reseting the WiFi credentials");
    writeStringToFlash("", 0);  // Reset the SSID
    writeStringToFlash("", 40); // Reset the Password
    writeStringToFlash("", 60); // Reset the Custom Data
    DEBUG_SERIAL.println("Wifi credentials erased and Custom Data erased");
    DEBUG_SERIAL.println("Restarting the ESP");
    delay(500);
    ESP.restart(); // Restart ESP
  }
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval)
  {
    sendRestful();
    sendData();
    previousMillis = currentMillis;
  }
}
void writeStringToFlash(const char *toStore, int startAddr)
{
  int i = 0;
  for (; i < LENGTH(toStore); i++)
  {
    EEPROM.write(startAddr + i, toStore[i]);
  }
  EEPROM.write(startAddr + i, '\0');
  EEPROM.commit();
}

String readStringFromFlash(int startAddr)
{
  char in[128]; // char array of size 128 for reading the stored data
  int i = 0;
  for (; i < 128; i++)
  {
    in[i] = EEPROM.read(startAddr + i);
  }
  return String(in);
}