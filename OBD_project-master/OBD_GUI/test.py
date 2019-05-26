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
import multiprocessing
from multiprocessing import Lock
import threading
from ctypes import c_bool
import time

d = multiprocessing.Value('i', 0)
flag = multiprocessing.Value(c_bool, False)
class main(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        global d
        global lock
        global flag
        self.d = d
        self.lock = lock
        self.flag = flag
    def run(self):
        # global flag
        processMehod()
        n=5
        while n>0:
            self.lock.acquire()
            time.sleep(1)
            self.d.value+=1
            self.flag.value = True
            self.lock.release()
            n-=1
        print(self.d.value)
        processMehod()
        if thredhold >1:
            thredhold+=1
            print("thredhold biggrt 1",thredhold)


class thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        global d
        global lock
        global flag
        print(flag.value)
        while True:
            lock.acquire()
            if d.value==3:
                print("detect event",str(d.value))
                time.sleep(1)
                print(flag.value)
            lock.release()

thredhold = 0

def processMehod():
    global thredhold
    thredhold += 1
    print("thredhold",str(thredhold))

def haha():
    m = main()
    m.start()
    t = thread()
    t.start()
    time.sleep(9)
    print("thredhold main", str(thredhold))
    print(d.value)
    m.join()
    t.join()



if __name__ == "__main__":
    v = 1


    lock = Lock()
    haha()

    # while True:
    #     if num.value==2:
    #         print(num.value)




