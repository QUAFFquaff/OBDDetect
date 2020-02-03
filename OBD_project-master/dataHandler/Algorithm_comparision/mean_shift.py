#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 1/4/2020 13:27
# @Author  : Haoyu Lyu
# @File    : mean_shift.py
# @Software: PyCharm

import numpy as np
import matplotlib.pyplot as plt

# Input data set
# X = np.array([
#     [-4, -3.5], [-3.5, -5], [-2.7, -4.5],
#     [-2, -4.5], [-2.9, -2.9], [-0.4, -4.5],
#     [-1.4, -2.5], [-1.6, -2], [-1.5, -1.3],
#     [-0.5, -2.1], [-0.6, -1], [0, -1.6],
#     [-2.8, -1], [-2.4, -0.6], [-3.5, 0],
#     [-0.2, 4], [0.9, 1.8], [1, 2.2],
#     [1.1, 2.8], [1.1, 3.4], [1, 4.5],
#     [1.8, 0.3], [2.2, 1.3], [2.9, 0],
#     [2.7, 1.2], [3, 3], [3.4, 2.8],
#     [3, 5], [5.4, 1.2], [6.3, 2]
# ])
from matplotlib.ticker import FuncFormatter
from mpl_toolkits.mplot3d import Axes3D


def read_txt():
    with open('../../data/fakeData0.txt', 'r') as f:
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

normal_events = ['a','h','v','o']
medium_events = ['b','i','p','w']
high_events = ['c','j','q','x']
def word2vector(word):
    x0,x1,x2 = 0, 0, 0
    for l in word:
        if l in normal_events:
            x0 += 1
        elif l in medium_events:
            x1 += 10
        elif l in high_events:
            x2 += 20
    return [x0,x1,x2,len(word)]

def build_matrix(document, input = []):
    for word in document:
        temp_v = word2vector(word)
        if temp_v not in input:
            input.append(temp_v)
    # print(input)
    return input

def mean_shift(data, radius=2.0):
    clusters = []
    for i in range(len(data)):
        cluster_centroid = data[i]
        cluster_frequency = np.zeros(len(data))

        # Search points in circle
        while True:
            temp_data = []
            for j in range(len(data)):
                v = data[j]
                # Handle points in the circles
                if np.linalg.norm(v - cluster_centroid) <= radius:
                    temp_data.append(v)
                    cluster_frequency[i] += 1

            # Update centroid
            old_centroid = cluster_centroid
            new_centroid = np.average(temp_data, axis=0)
            cluster_centroid = new_centroid
            # Find the mode
            if np.array_equal(new_centroid, old_centroid):
                break

        # Combined 'same' clusters
        has_same_cluster = False
        for cluster in clusters:
            if np.linalg.norm(cluster['centroid'] - cluster_centroid) <= radius:
                has_same_cluster = True
                cluster['frequency'] = cluster['frequency'] + cluster_frequency
                break

        if not has_same_cluster:
            clusters.append({
                'centroid': cluster_centroid,
                'frequency': cluster_frequency
            })

    clustering(data, clusters)
    print(cluster['centroid'])
    print('number of clusters: ',len(clusters))
    print('the items of each cluster is: ',len(clusters[0]['data']),len(clusters[1]['data']),len(clusters[2]['data']),len(clusters[3]['data']))
    show_clusters(clusters, radius,data)
    print(clusters[0]['data'])
    tests = ['h', 'a', 'qq', 'cx', 'hvh']
    for test in tests:
        test_model(test,clusters)



# Clustering data using frequency
def clustering(data, clusters):
    t = []
    for cluster in clusters:
        cluster['data'] = []
        t.append(cluster['frequency'])
    t = np.array(t)
    # Clustering
    for i in range(len(data)):
        column_frequency = t[:, i]
        cluster_index = np.where(column_frequency == np.max(column_frequency))[0][0]
        clusters[cluster_index]['data'].append(data[i])


# Plot clusters
def show_clusters(clusters, radius, X):
    colors = 10 * ['r', 'g', 'b', 'k', 'y']
    # plt.figure(figsize=(5, 5))
    # plt.xlim((-8, 8))
    # plt.ylim((-8, 8))
    # plt.scatter(X[:, 0], X[:, 1], s=20)
    # theta = np.linspace(0, 2 * np.pi, 800)
    # 3D
    fig = plt.figure()
    ax = Axes3D(fig)
    for i in range(len(clusters)):
        cluster = clusters[i]
        data = np.array(cluster['data'])
        # plt.scatter(data[:, 0], data[:, 1], color=colors[i], s=20)
        ax.scatter(data[:, 0],data[:, 1],data[:, 2], c=colors[i], label='first cluster')

    ax.legend(loc='best')
    ax.set_zlabel('high risk', fontdict={'size': 13, 'color': 'black'})
    ax.set_ylabel('medium risk', fontdict={'size': 13, 'color': 'black'})
    ax.set_xlabel('normal event', fontdict={'size': 13, 'color': 'black'})
    plt.savefig('fig.png', bbox_inches='tight')
    plt.show()

    plt.show()

def test_model(test,clusters):
    vect = np.array(word2vector(test))
    for i in range(len(clusters)):
        cluster = clusters[i]['data']
        for item in cluster:

            if item.tolist() == vect.tolist():
                print(test,' in cluster ',i)
                return

def main():
    documents = read_txt()
    input = []
    for i in documents:
        input = build_matrix(i,input)

    X = np.array(input)
    mean_shift(X, 35)

main()