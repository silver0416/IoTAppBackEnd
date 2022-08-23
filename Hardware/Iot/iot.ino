/**
 *
 *
 *
 */
#include <Arduino.h>
#include <WiFi.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>

const char *ssid = "your-ssid";
const char *password = "password";

WebSocketsClient webSocketClient;

WiFiClient client;

char path[] = "/ws/chat/temp/";

char host[] = "192.168.100.2";

const uint16_t port = 8000;

StaticJsonDocument<200> doc;

#define DEBUG_SERIAL Serial

#define USE_SERIAL Serial1

void hexdump(const void *mem, uint32_t len, uint8_t cols = 16)
{
    const uint8_t *src = (const uint8_t *)mem;
    USE_SERIAL.printf("\n[HEXDUMP] Address: 0x%08X len: 0x%X (%d)", (ptrdiff_t)src, len, len);
    for (uint32_t i = 0; i < len; i++)
    {
        if (i % cols == 0)
        {
            USE_SERIAL.printf("\n[0x%08X] 0x%08X: ", (ptrdiff_t)src, i);
        }
        USE_SERIAL.printf("%02X ", *src);
        src++;
    }
    USE_SERIAL.printf("\n");
}

void webSocketEvent(WStype_t type, uint8_t *payload, size_t length)
{

    switch (type)
    {
    case WStype_DISCONNECTED:
        USE_SERIAL.printf("[WSc] Disconnected!\n");
        break;
    case WStype_CONNECTED:
        USE_SERIAL.printf("[WSc] Connected to url: %s\n", payload);

        // send message to server when Connected
        // webSocketClient.sendTXT("Connected");
        break;
    case WStype_TEXT:
        USE_SERIAL.printf("[WSc] get text: %s\n", payload);

        // send message to server
        // webSocketClient.sendTXT("message here");
        break;
    case WStype_BIN:
        USE_SERIAL.printf("[WSc] get binary length: %u\n", length);
        hexdump(payload, length);

        // send data to server
        // webSocket.sendBIN(payload, length);
        break;
    case WStype_ERROR:
    case WStype_FRAGMENT_TEXT_START:
    case WStype_FRAGMENT_BIN_START:
    case WStype_FRAGMENT:
    case WStype_FRAGMENT_FIN:
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
    DEBUG_SERIAL.print("Waiting for WiFi... ");

    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.print(".");
        delay(500);
    }

    DEBUG_SERIAL.println("");
    DEBUG_SERIAL.println("WiFi connected");
    DEBUG_SERIAL.println("IP address: ");
    DEBUG_SERIAL.println(WiFi.localIP());

    delay(5000);
    if (client.connect(host, 8000))
    {
        Serial.println("connected");
    }
    else
    {
        Serial.println("not connected");
    }
    webSocketClient.begin(host,port,path);
    webSocketClient.onEvent(webSocketEvent);
    // webSocketClient.setReconnectInterval(5000);
}

void loop()
{
    webSocketClient.loop();

    // if (!client.connect(host, port))
    // {
    //     Serial.println("Connection failed.");
    //     Serial.println("Waiting 5 seconds before retrying...");
    //     delay(5000);
    //     return;
    // }
    // else if (!client.connected())
    // {
    //     Serial.print("Connecting to ");
    //     Serial.println(host);
    // }

    // // This will send a request to the server
    // // uncomment this line to send an arbitrary string to the server
    // // client.print("Send this data to the server");
    // // uncomment this line to send a basic document request to the server
    // client.print("Hello world!!");

    // int maxloops = 0;

    // // wait for the server's reply to become available
    // while (!client.available() && maxloops < 1000)
    // {

    //     maxloops++;
    //     delay(1); // delay 1 msec
    // }
    // if (client.available() > 0)
    // {
    //     // read back one line from the server
    //     String line = client.readStringUntil('\r');
    //     Serial.println(line);
    // }
    // else
    // {
    //     Serial.println("client.available() timed out ");
    // }

    // // Serial.println("Closing connection.");
    // // client.stop();

    // // Serial.println("Waiting 5 seconds before restarting...");
    // delay(1000);
}
