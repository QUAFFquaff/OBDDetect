import serial
import time
import numpy as np
import queue
import GUI
import threading
from scipy import signal
import pymysql
import pymysql.cursors
import joblib
import sys
import multiprocessing
from ctypes import c_bool

def connectDB():
    connection = pymysql.connect(host='35.197.95.95',
                                 user='root',
                                 password='obd12345',
                                 db='DRIVINGDB',
                                 port=3306,
                                 charset='utf8')
    return connection


try:
    # 获取一个游标
    connection = connectDB()
    connection.autocommit(True)


    mycursor = connection.cursor()
    sql = "INSERT INTO STATUS(VIN,DEVICEID,TIME,SPEED,PARAM_1,PARAM_2,PARAM_3,LONGITUDE,LATITUDE,GYROX,GYROY,GYROZ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (1, "zahraa", 1, 1, 1, 1, 1, "", "", 1, 1, 1)
    mycursor.execute(sql, val)
    mycursor.close()
finally:
    connection.close()