#include <WiFi.h>             // Include WIFi Library for ESP32
#include <WebServer.h>        // Include WebSwever Library for ESP32
#include <ArduinoJson.h>      // Include ArduinoJson Library
#include "DHT.h"              // Include DHT Library
#include <WebSocketsServer.h> // Include Websocket Library
#define DHTPIN 4              // Define DHTPIN
#define DHTTYPE DHT11         // Define DHTTYPE

// 輸入wifi的ssid與password
const char *ssid = "your-ssid";
const char *password = "your-password";

int interval = 1000;              // virtual delay
unsigned long previousMillis = 0; // Tracks the time since last event fired

String web = "<!DOCTYPE html><html><head> <title>Websocket</title> <meta name='viewport' content='width=device-width, initial-scale=1.0' /> <meta charset='UTF-8'> <style> body { background-color: #F7F9FD; text-align: center; } </style></head><body> <h1>Temperature: <span id='temp'>-</span></h1> <h1>Humidity: <span id='hum'>-</span></h1> <h1>Received message: <span id='message'>-</span></h1><button type='button' id='btnA'> <h1>ON</h1> </button><button type='button' id='btnB'> <h1>OFF</h1> </button></body><script> var Socket; document.getElementById('btnA').addEventListener('click', buttonApressed); document.getElementById('btnB').addEventListener('click', buttonBpressed); function init() { Socket = new WebSocket('ws://' + window.location.hostname + ':81/'); Socket.onmessage = function(event) { processReceivedCommand(event); }; } function processReceivedCommand(event) { var obj = JSON.parse(event.data); document.getElementById('message').innerHTML = obj.PIN_Status; document.getElementById('temp').innerHTML = obj.Temp; document.getElementById('hum').innerHTML = obj.Hum; console.log(obj.PIN_Status); console.log(obj.Temp); console.log(obj.Hum); } function buttonApressed() { Socket.send('1'); } function buttonBpressed() { Socket.send('0'); } window.onload = function(event) { init(); }</script></html>";
String jsonString;      // Temporary storage for the JSON String
String pin_status = ""; // Holds the status of the pin
float t;                // holds the temperature value
float h;                // holds the Humidity value

DHT dht(DHTPIN, DHTTYPE);                          // create instance for DHT sensor
WebServer server(80);                              // create instance for web server on port "80"
WebSocketsServer webSocket = WebSocketsServer(81); // create instance for webSocket server on port"81"

void setup()
{
  // put your setup code here, to run once:
  pinMode(2, OUTPUT);         // Set PIN22 As output(LED Pin)
  Serial.begin(115200);       // Init Serial for Debugging.
  WiFi.begin(ssid, password); // Connect to Wifi
  while (WiFi.status() != WL_CONNECTED)
  { // Check if wifi is connected or not
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  // Print the IP address in the serial monitor windows.
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  // Initialize a web server on the default IP address. and send the webpage as a response.
  server.on("/", []()
            { server.send(200, "text/html", web); });
  server.begin();                    // init the server
  webSocket.begin();                 // init the Websocketserver
  webSocket.onEvent(webSocketEvent); // init the webSocketEvent function when a websocket event occurs
  dht.begin();                       // Init DHT sensor
}

void loop()
{
  server.handleClient();                  // webserver methode that handles all Client
  webSocket.loop();                       // websocket server methode that handles all Client
  unsigned long currentMillis = millis(); // call millis  and Get snapshot of time
  if ((unsigned long)(currentMillis - previousMillis) >= interval)
  {                                 // How much time has passed, accounting for rollover with subtraction!
    update_temp_hum();              // update temperature data.
    update_webpage();               // Update Humidity Data
    previousMillis = currentMillis; // Use the snapshot to set track time until next event
  }
}

void webSocketEvent(byte num, WStype_t type, uint8_t *payload, size_t length)
{
  switch (type)
  {
  case WStype_DISCONNECTED: // enum that read status this is used for debugging.
    Serial.print("WS Type ");
    Serial.print(type);
    Serial.println(": DISCONNECTED");
    break;
  case WStype_CONNECTED: // Check if a WebSocket client is connected or not
    Serial.print("WS Type ");
    Serial.print(type);
    Serial.println(": CONNECTED");
    if (digitalRead(2) == HIGH)
    { // check if pin 22 is high or low
      pin_status = "ON";
      update_webpage(); // update the webpage accordingly
    }
    else
    {
      pin_status = "OFF"; // check if pin 22 is high or low
      update_webpage();   // update the webpage accordingly
    }
    break;
  case WStype_TEXT:   // check responce from client
    Serial.println(); // the payload variable stores teh status internally
    Serial.println(payload[0]);
    if (payload[0] == '1')
    {
      pin_status = "ON";
      digitalWrite(2, HIGH);
    }
    if (payload[0] == '0')
    {
      pin_status = "OFF";
      digitalWrite(2, LOW);
    }
    break;
  }
}
void update_temp_hum()
{
  h = dht.readHumidity();    // Read temperature as Celsius (the default)
  t = dht.readTemperature(); // Read temperature as Fahrenheit (isFahrenheit = true
}
void update_webpage()
{
  StaticJsonDocument<100> doc;
  // create an object
  JsonObject object = doc.to<JsonObject>();
  object["PIN_Status"] = pin_status;
  if (pin_status == "ON")
  {
    object["Temp"] = t;
    object["Hum"] = h;
  }
  else
  {
    object["Temp"] = "Nan";
    object["Hum"] = "Nan";
  }
  serializeJson(doc, jsonString);     // serialize the object and save teh result to teh string variable.
  Serial.println(jsonString);         // print the string for debugging.
  webSocket.broadcastTXT(jsonString); // broadcast the string to all connected clients.
  jsonString = "";                    // clear the String.
}
