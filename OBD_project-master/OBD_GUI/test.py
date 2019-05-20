import serial

ser = serial.Serial('/dev/rfcomm0',57600)

while True:
    result = ser.read()
    print (result)