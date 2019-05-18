from numpy import *

import pymysql
import pymysql.cursors


def connectDB():
    connection = pymysql.connect(host='35.197.95.95',
                                 user='root',
                                 password='obd12345',
                                 db='DRIVINGDB',
                                 port=3306,
                                 charset='utf8')
    return connection

timestamp = []
c = 20
try:
    newrecord = 0
    # 获取一个游标
    connection = connectDB()
    connection.autocommit(True)
    # with connection.cursor() as cursor:

    while c > 0:
        cursor = connection.cursor()
        sql = 'select * from STATUS ORDER BY time DESC LIMIT 1'
        count = cursor.execute(sql)
        data = cursor.fetchone()
        print(data)

        # i = 0
        # for row in cursor.fetchall():
        #     if i == 0:
        #         if row[2] != newrecord:  # detect if catch the same data
        #             isCatch = True
        #             newrecord = row[2]
        #             # print(newrecord)
        #     if isCatch:
        #         if(i==0):
        #             timestamp.append(row[2])
        #     i = i + 1
        # c = c-1
        # connection.commit()

    print (timestamp)
finally:
    connection.close()

