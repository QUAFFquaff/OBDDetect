#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 1/4/2020 3:15
# @Author  : Haoyu Lyu
# @File    : COP_Kmeans.py
# @Software: PyCharm

import numpy
from copkmeans.cop_kmeans import cop_kmeans

def read_txt():
    with open('../../../data/fakeData.txt', 'r') as f:
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


input_matrix = numpy.random.rand(100, 500)
input_matrix = read_txt()
print(input_matrix)
must_link = [(0, 10), (0, 20), (0, 30)]
cannot_link = [(1, 10), (2, 10), (3, 10)]
clusters, centers = cop_kmeans(dataset=input_matrix, k=5, ml=must_link,cl=cannot_link)