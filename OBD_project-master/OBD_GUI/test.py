# import serial
# import time
#
# ser = serial.Serial(port='/dev/rfcomm0',baudrate=57600,timeout = 0.5)
# print(ser)
# data = ''
# data = data.encode('utf-8')
# if not ser.is_open:
#     ser.open()
# n = ser.inWaiting()
# print('byte num:',str(n))
# while True:
#     obddata = data+ser.readline()
#     if obddata!=b'':
#         print('get data:',obddata)
#         millis = int(round(time.time()*1000))
#         print(millis)
obdData = b"Time,0,0.23,0.234,1.234,0.234,1.21,3.14"
row = obdData.split(b"\r")[0]
row = row.split(b",")
print(len(row))


