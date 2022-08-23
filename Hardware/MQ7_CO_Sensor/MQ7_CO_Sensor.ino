/*
  MQUnifiedsensor Library - reading an MQ7

  Demonstrates the use a MQ7 sensor.
  Library originally added 01 may 2019
  by Miguel A Califa, Yersson Carrillo, Ghiordy Contreras, Mario Rodriguez
 
  Added example
  modified 23 May 2019
  by Miguel Califa 

  Updated library usage
  modified 26 March 2020
  by Miguel Califa 

  Wiring:
  https://github.com/miguel5612/MQSensorsLib_Docs/blob/master/static/img/MQ_Arduino.PNG
  Please take care, arduino A0 pin represent the analog input configured on #define pin

 This example code is in the public domain.
 Soure: https://github.com/miguel5612/MQSensorsLib
*/


#include <MQUnifiedsensor.h>
MQUnifiedsensor MQ7("Arduino UNO", 5, 10, A0, "MQ-7");

void setup() {
  
  Serial.begin(9600);

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
  
}

void loop() {
  
  MQ7.update(); // Update data, the arduino will be read the voltage on the analog pin
  float COppm =MQ7.readSensor(); // Sensor will read PPM concentration using the model and a and b values setted before or in the setup
  Serial.print("CO= ");
  Serial.print(COppm);
  Serial.println(" ppm");
  delay(500); //Sampling frequency
  
}
