#include <Arduino.h>

//#define SEND_PWM_BY_TIMER         // Disable carrier PWM generation in software and use (restricted) hardware PWM.
//#define USE_NO_SEND_PWM           // Use no carrier PWM, just simulate an active low receiver signal. Overrides SEND_PWM_BY_TIMER definition
//#define NO_LED_FEEDBACK_CODE      // Saves 566 bytes program memory
//#define USE_OPEN_DRAIN_OUTPUT_FOR_SEND_PIN // Use or simulate open drain output mode at send pin. Attention, active state of open drain is LOW, so connect the send LED between positive supply and send pin!

#include "PinDefinitionsAndMore.h" // Define macros for input and output pin etc.
#include <IRremote.hpp>

void setup()
{
    pinMode(LED_BUILTIN, OUTPUT);

    Serial.begin(115200);
#if defined(__AVR_ATmega32U4__) || defined(SERIAL_PORT_USBVIRTUAL) || defined(SERIAL_USB) /*stm32duino*/ || defined(USBCON) /*STM32_stm32*/ || defined(SERIALUSB_PID) || defined(ARDUINO_attiny3217)
    delay(4000); // To be able to connect Serial monitor after reset or power up and before first print out. Do not wait for an attached Serial Monitor!
#endif
    // Just to know which program is running on my Arduino
    Serial.println(F("START " __FILE__ " from " __DATE__ "\r\nUsing library version " VERSION_IRREMOTE));

#if defined(IR_SEND_PIN)
    IrSender.begin(); // Start with IR_SEND_PIN as send pin and enable feedback LED at default feedback LED pin
#else
    IrSender.begin(3, ENABLE_LED_FEEDBACK); // Specify send pin and enable feedback LED at default feedback LED pin
#endif

    Serial.println(F("Ready to send IR signals at pin " STR(IR_SEND_PIN)));
}

void loop()
{

    /*
     * Send hand crafted data from RAM
     * The values are NOT multiple of 50, but are taken from the NEC timing definitions
     */
    Serial.println(F("Send Raw Data(16 bit array format)"));
    Serial.flush();

    const uint16_t rawData_close[199] = {4330, 4320, 580, 1570, 580, 520, 580, 1570, 580, 1570, 580, 520, 580, 470, 580, 1570, 580, 520, 580, 470, 630, 1570, 580, 470, 580, 520, 580, 1570, 580, 1570, 580, 520, 580, 1570, 580, 470, 580, 1570, 630, 1570, 580, 1570, 580, 1570, 580, 470, 630, 1570, 580, 1570, 580, 1570, 580, 520, 580, 470, 580, 520, 580, 470, 580, 1570, 630, 470, 580, 520, 580, 1570, 580, 1570, 580, 1570, 580, 520, 580, 470, 580, 520, 580, 470, 580, 520, 580, 470, 630, 470, 580, 520, 580, 1570, 580, 1570, 580, 1570, 580, 1570, 580, 1570, 630, 5070, 4380, 4270, 580, 1570, 580, 520, 580, 1570, 580, 1570, 580, 520, 580, 470, 580, 1570, 630, 470, 580, 470, 630, 1570, 580, 470, 580, 520, 580, 1570, 580, 1570, 580, 520, 580, 1570, 580, 470, 630, 1570, 580, 1570, 580, 1570, 580, 1570, 580, 520, 580, 1570, 580, 1570, 580, 1570, 580, 520, 580, 470, 580, 520, 580, 470, 580, 1570, 630, 470, 580, 520, 580, 1570, 580, 1570, 580, 1570, 580, 520, 580, 470, 580, 520, 580, 470, 580, 520, 580, 470, 630, 470, 580, 520, 580, 1570, 580, 1570, 580, 1570, 580, 1570, 580, 1570, 580};
    // const uint16_t rawData_open[199] = {4330, 4320, 530, 1620, 580, 520, 580, 1570, 580, 1570, 580, 520, 580, 470, 580, 1570, 530, 570, 530, 520, 580, 1620, 580, 470, 580, 570, 480, 1620, 580, 1570, 580, 520, 580, 1570, 580, 1570, 580, 520, 580, 1570, 580, 1570, 580, 1570, 580, 1570, 630, 1570, 580, 1570, 580, 470, 580, 1620, 580, 470, 580, 520, 580, 470, 630, 470, 580, 470, 630, 470, 580, 570, 480, 1620, 530, 520, 580, 1620, 580, 470, 530, 570, 580, 470, 580, 520, 580, 1570, 580, 520, 530, 1620, 580, 470, 580, 1620, 530, 1620, 530, 1620, 580, 1570, 580, 5070, 4380, 4320, 530, 1620, 580, 570, 480, 1620, 580, 1570, 580, 470, 630, 470, 530, 1620, 580, 520, 580, 470, 580, 1570, 580, 520, 580, 520, 580, 1570, 580, 1570, 580, 520, 580, 1570, 530, 1620, 580, 520, 580, 1570, 580, 1570, 580, 1570, 580, 1570, 580, 1570, 630, 1570, 530, 520, 580, 1570, 580, 520, 580, 470, 630, 470, 580, 520, 580, 470, 580, 520, 580, 470, 580, 1620, 530, 520, 530, 1620, 580, 520, 580, 520, 580, 470, 530, 570, 580, 1570, 580, 470, 630, 1570, 530, 520, 580, 1570, 630, 1570, 530, 1620, 580, 1570, 580};
    const uint16_t rawData_open[67] = {9980, 4420, 630, 620, 580, 620, 580, 670, 580, 570, 630, 620, 580, 620, 580, 670, 580, 1670, 630, 1670, 630, 1670, 630, 1670, 630, 1720, 580, 1770, 580, 1720, 580, 1720, 580, 620, 580, 620, 630, 1720, 580, 620, 580, 620, 630, 1720, 580, 620, 580, 620, 630, 620, 580, 1720, 580, 620, 580, 1720, 630, 1670, 630, 620, 580, 1770, 530, 1770, 580, 1670, 630}; // Protocol=NEC Address=0x80 Command=0x12 Raw-Data=0xED127F80 32 bits LSB first

    IrSender.sendRaw(rawData_open, sizeof(rawData_open) / sizeof(rawData_open[0]), NEC_KHZ); // Note the approach used to automatically calculate the size of the array.
    delay(1000);                                                                                // delay must be greater than 5 ms (RECORD_GAP_MICROS), otherwise the receiver sees it as one long signal
   
    delay(3000);                                                                               // Wait 60 seconds

    // IrSender.sendRaw(rawData_close, sizeof(rawData_close) / sizeof(rawData_close[0]), NEC_KHZ); // Note the approach used to automatically calculate the size of the array.
    // delay(1000); // delay must be greater than 5 ms (RECORD_GAP_MICROS), otherwise the receiver sees it as one long signal
    
    // delay(10000); // Wait 10 seconds
}
