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

obdData = b"sds,0,3.4\r\n"
row = obdData.split(b"\r")[0]
row = row.split(b",")
newrow = []
newrow.append(str(row[0],encoding="utf-8"))
newrow.append(int(str(row[1],encoding="utf-8")))
newrow.append(float(str(row[2],encoding="utf-8")))
print(newrow)