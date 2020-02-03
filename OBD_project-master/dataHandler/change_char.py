#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2/1/2020 13:28
# @Author  : Haoyu Lyu
# @File    : change_char.py
# @Software: PyCharm

def read_txt():
    with open('../data/dataNeedToBeScored.txt', 'r') as f:
        lines = f.readlines()
    file_list = []
    for line in lines:
        pattern_list = []
        patterns = line.split("\'")
        for i in range(len(patterns)):
            if i % 2 != 0:
                pattern_list.append(patterns[i])
        file_list.append(pattern_list)
    return file_list


def change_char(data):
    new_dacu = []

    for  line in data:
        new_line = []
        for pattern in line:
            new_pattern = ""
            for letter in pattern:
                new_letter = convert(letter)
                new_pattern += new_letter
            new_line.append(new_pattern)
        # print(line[:10],'  ',new_line[:10])
        new_dacu.append(new_line)

    print(new_dacu)
    write(str(new_dacu))

def write(data):
    try:
        with open('TOBESCORED.txt', 'w') as f:
            f.write(data)
    finally:
        if f:
            f.close()

def convert(letter):
    dic = {'a':'a','h':'b','v':'c','o':'d',
           'b':'m','i':'n','p':'o','w':'p',
           'c':'w','j':'x','q':'y','x':'z'}
    return dic[letter]

def main():
    data = read_txt()
    # data = [['a', 'h', 'ahhva', 'vvhha', 'oahooa',
    #          'b', 'abbw', 'ipi', 'bboi', 'paa',
    #          'p', 'ccw', 'jw', 'jiw', 'wwpwi',
    #          'c', 'jxxbx', 'qcxxqx', 'cqcqxqq', 'xcc']]
    # data = [['a', 'h', 'o', 'v','vo', 'hho','hhah','avoa','haa','vvvv', 'ova', 'avavv', 'ahao', 'aoah',],
    #                ['io', 'b', 'i',  'bi','va','vv','wwhhi','bbbi','abovb','ovppah','avhvowa','ai','ih','wa','ba'],
    #                ['iwwp', 'pb', 'pb', 'wbi', 'bi', 'p', 'pi', 'pwp' ,'xi','ixipp','bwbw', 'iwx','ibpxiix','iq','pq','px','ix','ipi','pwi'],
    #                ['xcqxx', 'cq',  'wx', 'cii','jcc', 'qq', 'jcxqc','cq', 'wj','j','q' 'jx', 'x', 'c', 'cjc']
    #                ]
    change_char(data)

main()