import serial

ser = serial.Serial(port='/dev/rfcomm0',baudrate=57600,timeout = 0.5)
print(ser)
data = ''
data = data.encode('utf-8')
if !ser.is_open:
    ser.open()
n = ser.inWaiting()
data = data+ser.readline()
print('get data:',data)
print(type(data))
