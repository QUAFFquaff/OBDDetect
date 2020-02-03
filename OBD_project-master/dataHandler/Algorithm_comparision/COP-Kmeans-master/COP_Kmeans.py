#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 1/4/2020 3:15
# @Author  : Haoyu Lyu
# @File    : COP_Kmeans.py
# @Software: PyCharm

import numpy as np
from copkmeans.cop_kmeans import cop_kmeans

import matplotlib.pyplot as plt

# input_matrix = np.random.rand(90, 5)
# print(input_matrix)
# must_link = [(0, 1), (0, 20), (0, 30)]
# cannot_link = [(1, 10), (2, 10), (3, 10)]
# clusters, centers = cop_kmeans(dataset=input_matrix, k=5, ml=must_link,cl=cannot_link)
# print(clusters)
# print(len(clusters))
from mpl_toolkits.mplot3d import Axes3D

import xlrd
import xlwt
from xlutils.copy import copy

def read_txt(path = '../../../data/ABCD0001.txt'):
    # was used newfakedata0.txt before Feb 2020
    with open(path, 'r') as f:
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


normal_events = ['a', 'b', 'c', 'd']
medium_events = ['m', 'n', 'o', 'p']
high_events = ['w', 'x', 'y', 'z']


def word2vector(word):
    x0, x1, x2 = 0, 0, 0
    for l in word:
        if l in normal_events:
            x0 += 1
        elif l in medium_events:
            x1 += 10
        elif l in high_events:
            x2 += 20
    return [x0, x1, x2, len(word)]


def build_matrix(document, input=[]):
    for word in document:
        temp_v = word2vector(word)
        if temp_v not in input:
            input.append(temp_v)
    # print(input)
    return input


def write_excel_xls(path, sheet_name, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    for name in sheet_name:
        sheet = workbook.add_sheet(name)  # 在工作簿中新建一个表格
        for i in range(0, index):
            for j in range(0, len(value[i])):
                sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿
    print("xls格式表格写入数据成功！")


def write_excel_xls_append(path, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i + rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")


book_name_xls = 'COP_Kmeans_result0001.xls'

sheet_name_xls = ['tests']


value_title = [["test case", "score", "cluster","index","vector"], ]

def cop_kmean():
    # input_matrix = numpy.random.rand(100, 500)
    documents = read_txt()
    input_matrix = []
    for i in documents:
        input_matrix = build_matrix(i, input_matrix)

    # must_link = [(1,2),(8,9),(0,1),(3,7),(0,3),(0,4),(11,12),(24,26),(25,27),(50,51),(53,54)]
    # cannot_link = [(7,13),(0,5),(0,8),(0,24),(0,27),(0,50),(0,53)]
    must_link = [(0,1),(0,2),(0,3),(0,7),(5,8), (14,18), (37,38)]
    cannot_link = [(0,4), (0,5), (0,6), (0,8), (7,71), (7,16), (0,31),(0,37),(7,123), (0,123), (7,18)]
    clusters, centers = cop_kmeans(dataset=input_matrix, k=4, ml=must_link, cl=cannot_link)
    print(clusters)
    print(input_matrix)
    print(centers)
    print(len(clusters) , '--',len(input_matrix))

    # test model
    # tests = ['h', 'a', 'qq', 'cx', 'hvh']
    tests = ['a', 'b', 'abbca', 'ccbba', 'dabdda',
                 'm', 'ammp', 'non', 'mmdn', 'oaa',
                 'o', 'wwp', 'xp', 'xnp', 'ppopn',
                 'w', 'xzzmz', 'ywzzyz', 'wywyzyy', 'zww']
    result = []
    for test in tests:
        vect = word2vector(test)
        temp = input_matrix.index(vect)
        # print(vect)
        group_num = clusters[temp]
        # print(test_result)

        line = [test,str(get_score(centers,vect,group_num)),str(group_num),str(temp),str(vect)]
        result.append(line)
    write_excel_xls(book_name_xls, sheet_name_xls, value_title)
    write_excel_xls_append(book_name_xls, result)
    # score_a_file(input_matrix, clusters, centers)

    fig = plt.figure()
    ax = Axes3D(fig)
    cluster_set = [[],[],[],[]]
    for ind in range(len(input_matrix)):
        cluster_set[clusters[ind]].append((input_matrix[ind]))
    cluster_arr = tuple(cluster_set)
    ax.scatter([i[0] for i in cluster_arr[0]],[i[1] for i in cluster_arr[0]],[i[2] for i in cluster_arr[0]], c='r', label='first cluster')
    ax.scatter([i[0] for i in cluster_arr[1]],[i[1] for i in cluster_arr[1]],[i[2] for i in cluster_arr[1]], c='b', label='second cluster')
    ax.scatter([i[0] for i in cluster_arr[2]],[i[1] for i in cluster_arr[2]],[i[2] for i in cluster_arr[2]], c='g', label='third cluster')
    ax.scatter([i[0] for i in cluster_arr[3]],[i[1] for i in cluster_arr[3]],[i[2] for i in cluster_arr[3]], c='y', label='fourth cluster')
    print('the items of each cluster is: ',len(cluster_set[3][:]),len(cluster_set[2]),len(cluster_set[1]),len(cluster_set[0]))
    # ax.scatter(centers[0][2], centers[0][3], centers[0][5], marker='*', c='r')
    # ax.scatter(centers[1][2], centers[1][3], centers[1][5], marker='1', c='b')
    # ax.scatter(centers[2][2], centers[2][3], centers[2][5], marker='P', c='g')
    # ax.scatter(centers[3][2], centers[3][3], centers[3][5], marker='x', c='y')
    # print(cluster_arr[0])
    ax.legend(loc='best')
    ax.set_zlabel('high risk', fontdict={'size': 13, 'color': 'black'})
    ax.set_ylabel('medium risk', fontdict={'size': 13, 'color': 'black'})
    ax.set_xlabel('normal event', fontdict={'size': 13, 'color': 'black'})
    plt.savefig('fig.png', bbox_inches='tight')
    plt.show()

def get_score(centers,point,group_num):
    distance = []
    for item in centers:
        d = 0
        for i in item:
            d += i*i
        distance.append(d)
    sort_distance = sorted(distance)

    dis_p = 0
    for i in point:
        dis_p += i*i

    # print(sort_distance)
    # 90    70  50  30
    # if dis_p<=sort_distance[0]:
    #     score = 100 - dis_p/sort_distance[0] * 10
    #     return score
    # elif dis_p>=sort_distance[0] and dis_p<=sort_distance[1]:
    #     score = 90 - (dis_p-sort_distance[0])/(sort_distance[1]-sort_distance[0]) * 20
    # elif sort_distance[1]<=dis_p<=sort_distance[2]:
    #     score = 70 - (dis_p-sort_distance[1])/(sort_distance[2]-sort_distance[1]) * 20
    # elif sort_distance[2]<=dis_p<=sort_distance[3]:
    #     score = 50 - (dis_p-sort_distance[2])/(sort_distance[3]-sort_distance[2]) * 20
    # elif sort_distance[3]<=dis_p:
    #     score = 30 - (dis_p-sort_distance[3])/sort_distance[3] * 80
    # print(sort_distance)
    # 85    70  50  30
    # if dis_p<=sort_distance[0]:
    #     score = 100 - dis_p/sort_distance[0] * 15
    #     return score
    # elif dis_p>=sort_distance[0] and dis_p<=sort_distance[1]:
    #     score = 85 - (dis_p-sort_distance[0])/(sort_distance[1]-sort_distance[0]) * 15
    # elif sort_distance[1]<=dis_p<=sort_distance[2]:
    #     score = 70 - (dis_p-sort_distance[1])/(sort_distance[2]-sort_distance[1]) * 20
    # elif sort_distance[2]<=dis_p<=sort_distance[3]:
    #     score = 50 - (dis_p-sort_distance[2])/(sort_distance[3]-sort_distance[2]) * 20
    # elif sort_distance[3]<=dis_p:
    #     score = 30 - (dis_p-sort_distance[3])/sort_distance[3] * 80
    # print(sort_distance)
    # 80    60  45  30
    # if dis_p<=sort_distance[0]:
    #     score = 100 - dis_p/sort_distance[0] * 20
    #     return score
    # elif dis_p>=sort_distance[0] and dis_p<=sort_distance[1]:
    #     score = 80 - (dis_p-sort_distance[0])/(sort_distance[1]-sort_distance[0]) * 20
    # elif sort_distance[1]<=dis_p<=sort_distance[2]:
    #     score = 60 - (dis_p-sort_distance[1])/(sort_distance[2]-sort_distance[1]) * 15
    # elif sort_distance[2]<=dis_p<=sort_distance[3]:
    #     score = 45 - (dis_p-sort_distance[2])/(sort_distance[3]-sort_distance[2]) * 15
    # elif sort_distance[3]<=dis_p:
    #     score = 30 - (dis_p-sort_distance[3])/sort_distance[3] * 80

    # generate method 2, based on cluster.
    # 80    60  45  30
    score = 100 - dis_p/sort_distance[0] * 20 * (group_num+1)

    return score


def score_a_file(input_matrix,clusters,centers):
    tests = read_txt('TOBESCORED.txt')
    result = []
    for test in tests:
        line = []
        for pattern in test:
            vect = word2vector(pattern)
            if vect in input_matrix:
                temp = input_matrix.index(vect)
                # print(vect)
                group_num = clusters[temp]
                # print(test_result)
                print('score is: ', get_score(centers, vect,group_num))

                line.append(get_score(centers, vect))
            else:
                line.append(0)
        result.append(line)
    write(str(result))

def write(data):
    try:
        with open('ScoredPattern.txt', 'w') as f:
            f.write(data)
    finally:
        if f:
            f.close()




cop_kmean()
