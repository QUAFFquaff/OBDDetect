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


def read_txt():
    with open('../../../data/fakeData0.txt', 'r') as f:
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


normal_events = ['a', 'h', 'v', 'o']
medium_events = ['b', 'i', 'p', 'w']
high_events = ['c', 'j', 'q', 'x']


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


def cop_kmean():
    # input_matrix = numpy.random.rand(100, 500)
    documents = read_txt()
    input_matrix = []
    for i in documents:
        input_matrix = build_matrix(i, input_matrix)

    print(input_matrix[70:])
    must_link = [(1,2),(8,9),(0,1),(3,7),(0,3),(0,4),(11,12),(24,26),(25,27),(50,51),(53,54)]
    cannot_link = [(7,13),(0,5),(0,8),(0,24),(0,27),(0,50),(0,53)]
    clusters, centers = cop_kmeans(dataset=input_matrix, k=4, ml=must_link, cl=cannot_link)
    print(clusters)
    print(input_matrix)
    print(len(clusters) , '--',len(input_matrix))

    # test model
    # tests = ['h', 'a', 'qq', 'cx', 'hvh']
    tests = ['h', 'a', 'qq', 'cx', 'hvh','xcqxx','ibpxiix','avhvowa']
    for test in tests:
        vect = word2vector(test)
        temp = input_matrix.index(vect)
        # print(temp)
        test_result = clusters[temp]
        # print(test_result)
        print('test case',test, 'in cluster ', test_result)



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


cop_kmean()
