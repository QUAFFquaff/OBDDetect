#!/usr/bin/env python

# encoding: utf-8

'''

@author: Quaff

@contact: Quaff.lyu@gmail.com

@file: makeData.py

@time: 2019/6/3 2:41

@desc:

'''
import random
import logging .config
import logging
import logging
from logging import handlers

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射

    def __init__(self,filename,level='info',when='D',backCount=3,fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)

def test_log():
    log = Logger('all.log',level='debug')
    log.logger.debug('debug')
    log.logger.info('info')
    log.logger.warning('警告')
    log.logger.error('报错')
    log.logger.critical('严重')
    Logger('error.log', level='error').logger.error('error')

logging.basicConfig(level=logging.INFO,#控制台打印的日志级别
                    filename='new.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )
notebook = "ahovbipwcjqx"


def makeLevel0():
    length = int(random.gauss(2.5, 2))
    if length <= 0:
        return "!"
    term = ''
    for i in range(length):
        threshold = random.randint(0, 99)
        if threshold != 9:
            index = random.randint(0, 3)
            term += notebook[index]
        else:
            term += notebook[random.randint(4, 11)]
    return "'" + term + "'"


def makeLevel1():
    length = int(random.gauss(2.5, 2))
    if length <= 0:
        return "!"
    term = ''
    for i in range(length):
        threshold = random.randint(0, 99)
        if threshold < 30:
            index = random.randint(0, 3)
            term += notebook[index]
        else:
            term += notebook[random.randint(4, 7)]
    return "'" + term + "'"

def makeLevel2():
    length = int(random.gauss(3.5, 1.5))
    if length <= 0:
        return "!"
    term = ''
    for i in range(length):
        threshold = random.randint(0, 99)
        if threshold < 10:
            index = random.randint(0, 11)
            term += notebook[index]
        elif threshold > 75:
            term += notebook[random.randint(4, 11)]
        else:
            term += notebook[random.randint(4, 7)]
    return "'" + term + "'"

def makeLevel3():
    length = int(random.gauss(3, 1.9))
    if length <= 0:
        return "!"
    term = ''
    for i in range(length):
        threshold = random.randint(0, 99)
        if threshold < 10:
            index = random.randint(4, 7)
            term += notebook[index]
        else:
            term += notebook[random.randint(8, 11)]
    return "'" + term + "'"




def makeDocument(level):
    document = '['
    for i in range(100):
        if level == 0:
            temp = makeLevel0()
        elif level == 1:
            temp = makeLevel1()
        elif level == 2:
            temp = makeLevel2()
        elif level == 3:
            temp = makeLevel3()
        if temp == "!": continue
        document += temp + ", "
    return document + "]"


def main():
    data = ""

    log = Logger('all.log',level='debug')
    for j in range(4):
        for i in range(50):
            data += makeDocument(j) + ",\n"
    write(data)
    data1 = readText()
    log.logger.info("test")


def write(data):
    try:
        with open('fakeData.txt', 'w') as f:
            f.write(data)
    finally:
        if f:
            f.close()


def readText():
    try:
        f = open('fakeData.txt', 'r')  # 打开文件
        data = f.read()  # 读取文件内容
        # print(data)
        logging.info(data)
        # return data[0]
    finally:
        if f:
            f.close()
            return


main()
