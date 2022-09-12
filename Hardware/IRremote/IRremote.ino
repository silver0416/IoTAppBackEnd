#include <IRremote.h>

#define DELAY_AFTER_SEND 10000
#define DELAY_AFTER_LOOP 5000
uint16_t rawData_open[199] = {4330, 4320, 530, 1620, 580, 520, 580, 1570, 580, 1570, 580, 520, 580, 470, 580, 1570, 530, 570, 530, 520, 580, 1620, 580, 470, 580, 570, 480, 1620, 580, 1570, 580, 520, 580, 1570, 580, 1570, 580, 520, 580, 1570, 580, 1570, 580, 1570, 580, 1570, 630, 1570, 580, 1570, 580, 470, 580, 1620, 580, 470, 580, 520, 580, 470, 630, 470, 580, 470, 630, 470, 580, 570, 480, 1620, 530, 520, 580, 1620, 580, 470, 530, 570, 580, 470, 580, 520, 580, 1570, 580, 520, 530, 1620, 580, 470, 580, 1620, 530, 1620, 530, 1620, 580, 1570, 580, 5070, 4380, 4320, 530, 1620, 580, 570, 480, 1620, 580, 1570, 580, 470, 630, 470, 530, 1620, 580, 520, 580, 470, 580, 1570, 580, 520, 580, 520, 580, 1570, 580, 1570, 580, 520, 580, 1570, 530, 1620, 580, 520, 580, 1570, 580, 1570, 580, 1570, 580, 1570, 580, 1570, 630, 1570, 530, 520, 580, 1570, 580, 520, 580, 470, 630, 470, 580, 520, 580, 470, 580, 520, 580, 470, 580, 1620, 530, 520, 530, 1620, 580, 520, 580, 520, 580, 470, 530, 570, 580, 1570, 580, 470, 630, 1570, 530, 520, 580, 1570, 630, 1570, 530, 1620, 580, 1570, 580};
uint16_t rawData_close[199] = {4330, 4320, 580, 1570, 580, 520, 580, 1570, 580, 1570, 580, 520, 580, 470, 580, 1570, 580, 520, 580, 470, 630, 1570, 580, 470, 580, 520, 580, 1570, 580, 1570, 580, 520, 580, 1570, 580, 470, 580, 1570, 630, 1570, 580, 1570, 580, 1570, 580, 470, 630, 1570, 580, 1570, 580, 1570, 580, 520, 580, 470, 580, 520, 580, 470, 580, 1570, 630, 470, 580, 520, 580, 1570, 580, 1570, 580, 1570, 580, 520, 580, 470, 580, 520, 580, 470, 580, 520, 580, 470, 630, 470, 580, 520, 580, 1570, 580, 1570, 580, 1570, 580, 1570, 580, 1570, 630, 5070, 4380, 4270, 580, 1570, 580, 520, 580, 1570, 580, 1570, 580, 520, 580, 470, 580, 1570, 630, 470, 580, 470, 630, 1570, 580, 470, 580, 520, 580, 1570, 580, 1570, 580, 520, 580, 1570, 580, 470, 630, 1570, 580, 1570, 580, 1570, 580, 1570, 580, 520, 580, 1570, 580, 1570, 580, 1570, 580, 520, 580, 470, 580, 520, 580, 470, 580, 1570, 630, 470, 580, 520, 580, 1570, 580, 1570, 580, 1570, 580, 520, 580, 470, 580, 520, 580, 470, 580, 520, 580, 470, 630, 470, 580, 520, 580, 1570, 580, 1570, 580, 1570, 580, 1570, 580, 1570, 580};
void setup()
{
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

#if defined(IR_SEND_PIN)
    Serial.println(F("Ready to send IR signals at pin " STR(IR_SEND_PIN)));
#else
    Serial.println(F("Ready to send IR signals at pin 3"));
#endif

#if !defined(SEND_PWM_BY_TIMER)
    /*
     * Print internal signal generation info
     */
    IrSender.enableIROut(38); // Call it with 38 kHz to initialize the values printed below
    Serial.print(F("Send signal mark duration is "));
    Serial.print(IrSender.periodOnTimeMicros);
    Serial.print(F(" us, pulse correction is "));
    Serial.print(IrSender.getPulseCorrectionNanos());
    Serial.print(F(" ns, total period is "));
    Serial.print(IrSender.periodTimeMicros);
    Serial.println(F(" us"));
#endif
}

void loop()
{
    //  IrSender.sendNEC(0xB24D7B84
    // & 0xFF,32);
    IrSender.sendRaw(rawData_open, sizeof(rawData_open) / sizeof(int), 38);
    delay(DELAY_AFTER_SEND); // delay must be greater than 5 ms (RECORD_GAP_MICROS), otherwise the receiver sees it as one long signal
    IrSender.sendRaw(rawData_close, sizeof(rawData_close) / sizeof(int), 38);
    delay(DELAY_AFTER_SEND); // delay must be greater than 5 ms (RECORD_GAP_MICROS), otherwise the receiver sees it as one long signal
}
