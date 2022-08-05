import serial
import time
import connectMySQL
import database

dbConn = connectMySQL.connectMySQL()
# open a cursor to the database
cursor = dbConn.cursor()

device = 'COM4'  # this will have to be changed to the serial port you are using
try:
    print("Trying...", device)
    arduino = serial.Serial(device, 9600)
except:
    print("Failed to connect on", device)


countdown = 3
while True:
    data = arduino.readline().decode('utf-8').split('\t')
    if countdown == 0:
        time.sleep(120) # read the data from the arduino
        Humidity = data[0][10:14]
        Temperature = data[1][13:17]
        print(Humidity, Temperature)
        database.dataStorage.dht11_data_store(Humidity, Temperature, '1')
    else:
        countdown = countdown - 1
