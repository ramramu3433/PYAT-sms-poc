import serial

ser = serial.Serial('/dev/ttyUSB1', 115200)
ser.write("AT+CREG?\r")
response =  ser.read(2)
print response
ser.close()
