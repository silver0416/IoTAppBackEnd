#include "WiFi.h"
#include "EEPROM.h"
#include "HTTPClient.h"
#include "ArduinoJson.h"
#include "Arduino.h"
#define LENGTH(x) (strlen(x) + 1) // length of char string
#define EEPROM_SIZE 200           // EEPROM size
#define WiFi_rst 0                // WiFi credential reset pin (Boot button on ESP32)
String ssid;                      // string variable to store ssid
String pss;                       // string variable to store password
String customData;
char *aes = "McQfTjWnZr4u7x!A"; // AES key
unsigned long rst_millis;
#define DEBUG_SERIAL Serial
HTTPClient http;
StaticJsonDocument<200> doc;
StaticJsonDocument<200> doc2;
String jsonString;
String jsonString1;
int interval = 60000;
unsigned long previousMillis = 0;
String request = "http://192.168.1.14:8000/auth/device_data/";

#include <MQUnifiedsensor.h>
MQUnifiedsensor MQ7("ESP-32", 3.3, 12, 32, "MQ-7");
float COppm;


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
      // DEBUG_SERIAL.write(rvd_data, 33);
      // DEBUG_SERIAL.printf("\n");
    }
  }
  break;
  }
}

void sendData(){
  JsonObject root = doc.to<JsonObject>();
  JsonObject root1 = doc2.to<JsonObject>();
  if (digitalRead(LED_BUILTIN) == HIGH)
  {
    MQ7.update();                   // Update data, the arduino will be read the voltage on the analog pin
    COppm = MQ7.readSensor(); // Sensor will read PPM concentration using the model and a and b values setted before or in the setup
  }
  doc2["COppm"] = COppm;
  serializeJson(doc2, jsonString1);
  doc["data_status"] = jsonString1;
  doc["home"] = customData.substring(0, 8);
  doc["device"] = customData.substring(8, 44);
  doc["user"] = customData.substring(44, customData.length());
  serializeJson(doc, jsonString);
  http.addHeader("Content-Type", "application/json");
  http.POST(jsonString);
  DEBUG_SERIAL.println(jsonString);
  DEBUG_SERIAL.println(doc["data_status"].as<String>().c_str());
  jsonString = "";
  jsonString1 = "";
}

void setup() {

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
    digitalWrite(LED_BUILTIN, HIGH); // Turn on LED
  }
  
  MQ7.setRegressionMethod(1); //_PPM =  a*ratio^b
  MQ7.setA(99.042); MQ7.setB(-1.518); // Configurate the ecuation values to get CO concentration
  MQ7.init(); 

  Serial.print("Calibrating please wait.");
  float calcR0 = 0;
  for(int i = 1; i<=10; i ++)
  {
    MQ7.update(); // Update data, the arduino will be read the voltage on the analog pin
    calcR0 += MQ7.calibrate(27.5);
    Serial.print(".");
  }
  MQ7.setR0(calcR0/10);
  Serial.println("  done!.");
  if(isinf(calcR0)) {Serial.println("Warning: Conection issue founded, R0 is infite (Open circuit detected) please check your wiring and supply"); while(1);}
  if(calcR0 == 0){Serial.println("Warning: Conection issue founded, R0 is zero (Analog pin with short circuit to ground) please check your wiring and supply"); while(1);}
  MQ7.serialDebug(true);
  http.addHeader("Content-Type", "application/json");
  http.begin(request);
  
}

void loop() {

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
