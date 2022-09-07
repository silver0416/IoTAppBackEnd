
/*
  Date: 11-08-21
  Code is written by: Dharmik
  Configure ESP32 Wi-Fi parameters using SmartConfig
  Find more on www.TechTOnions.com
*/
#include "WiFi.h"
#include "EEPROM.h"
#include "HTTPClient.h"
#include "ArduinoJson.h"
#include "DHT.h"
#include "Arduino.h"
#define LENGTH(x) (strlen(x) + 1) // length of char string
#define EEPROM_SIZE 200           // EEPROM size
#define WiFi_rst 0                // WiFi credential reset pin (Boot button on ESP32)
String ssid;                      // string variable to store ssid
String pss;                       // string variable to store password
char *aes = "McQfTjWnZr4u7x!A";   // AES key
unsigned long rst_millis;

const String TYPE="DHT11";        // Device type
#define DHTPIN 4                  // DHT11 data pin
#define DHTTYPE DHT11             // DHT11 sensor type
DHT dht(DHTPIN, DHTTYPE);         // DHT11 sensor object

// 宣告讀取溫溼度的變數
StaticJsonDocument<100> doc;
String jsonString;
float temperature;
float humidity;
int interval = 60000;
unsigned long previousMillis = 0;

void WiFiEvent(WiFiEvent_t event, WiFiEventInfo_t info)
{
  Serial.printf("[WiFi-event] event: %d\n", event);

  switch (event)
  {

  case ARDUINO_EVENT_SC_SCAN_DONE:
  {
    Serial.println("Scan done");
  }
  break;

  case ARDUINO_EVENT_SC_FOUND_CHANNEL:
  {
    Serial.println("Found channel");
  }
  break;

  case ARDUINO_EVENT_SC_GOT_SSID_PSWD:
  {
    Serial.println("Got SSID and password");

    uint8_t ssid[33] = {0};
    uint8_t password[65] = {0};

    uint8_t rvd_data[33] = {0};

    memcpy(ssid, info.sc_got_ssid_pswd.ssid, sizeof(info.sc_got_ssid_pswd.ssid));
    memcpy(password, info.sc_got_ssid_pswd.password, sizeof(info.sc_got_ssid_pswd.password));

    Serial.printf("SSID:%s\n", ssid);
    Serial.printf("PASSWORD:%s\n", password);

    if (info.sc_got_ssid_pswd.type == SC_TYPE_ESPTOUCH_V2)
    {
      ESP_ERROR_CHECK(esp_smartconfig_get_rvd_data(rvd_data, sizeof(rvd_data)));

      Serial.println("RVD_DATA");
      Serial.write(rvd_data, 33);
      Serial.printf("\n");

      for (int i = 0; i < 33; i++)
      {
        Serial.printf("%02x ", rvd_data[i]);
      }
      Serial.printf("\n");
    }
  }
  break;

  case ARDUINO_EVENT_SC_SEND_ACK_DONE:
  {
    Serial.println("SC_EVENT_SEND_ACK_DONE");
  }
  break;

  default:
  {
    Serial.printf("no case event: %d\n", event);
  }
  break;
  }
}

void setup()
{
  Serial.begin(115200);           // Init serial
  pinMode(LED_BUILTIN, OUTPUT);   // Init LED
  digitalWrite(LED_BUILTIN, LOW); // Turn off LED
  pinMode(WiFi_rst, INPUT);
  if (!EEPROM.begin(EEPROM_SIZE))
  { // Init EEPROM
    Serial.println("failed to init EEPROM");
    delay(1000);
  }
  else
  {
    ssid = readStringFromFlash(0); // Read SSID stored at address 0
    Serial.print("SSID = ");
    Serial.println(ssid);
    pss = readStringFromFlash(40); // Read Password stored at address 40
    Serial.print("psss = ");
    Serial.println(pss);
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
    Serial.println("Waiting for SmartConfig.");
    while (!WiFi.smartConfigDone())
    {
      delay(500);
      Serial.print(".");
    }

    Serial.println("");
    Serial.println("SmartConfig received.");

    // Wait for WiFi to connect to AP
    Serial.println("Waiting for WiFi");
    while (WiFi.status() != WL_CONNECTED)
    {
      delay(500);
      Serial.print(".");
    }
    digitalWrite(LED_BUILTIN, HIGH); // Turn on LED
    Serial.println("WiFi Connected.");

    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());

    // read the connected WiFi SSID and password
    ssid = WiFi.SSID();
    pss = WiFi.psk();
    Serial.print("SSID:");
    Serial.println(ssid);
    Serial.print("PSS:");
    Serial.println(pss);
    Serial.println("Store SSID & PSS in Flash");
    writeStringToFlash(ssid.c_str(), 0); // storing ssid at address 0
    writeStringToFlash(pss.c_str(), 40); // storing pss at address 40
  }
  else
  {
    Serial.println("WiFi Connected");
    digitalWrite(LED_BUILTIN, HIGH); // Turn on LED
  }
}

void loop()
{
  // put your main code here, to run repeatedly:
  rst_millis = millis();
  while (digitalRead(WiFi_rst) == LOW)
  {
    // Wait till boot button is pressed
  }
  // check the button press time if it is greater than 3sec clear wifi cred and restart ESP
  if (millis() - rst_millis >= 3000)
  {
    Serial.println("Reseting the WiFi credentials");
    writeStringToFlash("", 0);  // Reset the SSID
    writeStringToFlash("", 40); // Reset the Password
    Serial.println("Wifi credentials erased");
    Serial.println("Restarting the ESP");
    delay(500);
    ESP.restart(); // Restart ESP
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
