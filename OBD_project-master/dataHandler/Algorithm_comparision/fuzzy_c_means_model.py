#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 1/20/2020 0:18
# @Author  : Haoyu Lyu
# @File    : fuzzy_c_means_model.py
# @Software: PyCharm


from fcmeans import FCM
from sklearn.datasets import make_blobs
from matplotlib import pyplot as plt
from seaborn import scatterplot as scatter
import numpy as np

from mpl_toolkits.mplot3d import Axes3D

# create artifitial dataset
# n_samples = 50000
# n_bins = 3  # use 3 bins for calibration_curve as we have 3 clusters here
# centers = [(-5, -5), (0, 0), (5, 5)]
#
# X,_ = make_blobs(n_samples=n_samples, n_features=2, cluster_std=1.0,
#                   centers=centers, shuffle=False, random_state=42)

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
            x1 += 5
        elif l in high_events:
            x2 += 10
    return [x0,x1,x2,len(word)]

def build_matrix(document, input = []):
    for word in document:
        temp_v = word2vector(word)
        if temp_v not in input:
            input.append(temp_v)
    # print(input)
    return input

def fuzzy(X):

    # X = np.array([(1,1),(1,2),(1,3),(2,2),(10,10),(100,100),(101,101),(102,102)])
    # print(X.type)
    # fit the fuzzy-c-means
    fcm = FCM(n_clusters=4)
    fcm.fit(X)

    # outputs
    fcm_centers = fcm.centers
    fcm_labels  = fcm.u.argmax(axis=1)

    print(fcm_labels)

    # plot result
    # %matplotlib inline
    f, axes = plt.subplots(1, 2, figsize=(11,5))
    scatter(X[:,0], X[:,1], ax=axes[0])
    scatter(X[:,0], X[:,1], ax=axes[1], hue=fcm_labels)
    scatter(fcm_centers[:,0], fcm_centers[:,1], ax=axes[1],marker="s",s=200)
    plt.show()
    show_clusters(fcm_labels,X)


# Plot clusters
def show_clusters(clusters,input_matrix):
    fig = plt.figure()
    ax = Axes3D(fig)
    cluster_set = [[], [], [], []]
    for ind in range(len(input_matrix)):
        cluster_set[clusters[ind]].append((input_matrix[ind]))
    cluster_arr = tuple(cluster_set)
    ax.scatter([i[0] for i in cluster_arr[0]], [i[1] for i in cluster_arr[0]], [i[2] for i in cluster_arr[0]], c='r',
               label='first cluster')
    ax.scatter([i[0] for i in cluster_arr[1]], [i[1] for i in cluster_arr[1]], [i[2] for i in cluster_arr[1]], c='b',
               label='second cluster')
    ax.scatter([i[0] for i in cluster_arr[2]], [i[1] for i in cluster_arr[2]], [i[2] for i in cluster_arr[2]], c='g',
               label='third cluster')
    ax.scatter([i[0] for i in cluster_arr[3]], [i[1] for i in cluster_arr[3]], [i[2] for i in cluster_arr[3]], c='y',
               label='fourth cluster')
    print('the items of each cluster is: ', len(cluster_set[3][:]), len(cluster_set[2]), len(cluster_set[1]),
          len(cluster_set[0]))

    ax.legend(loc='best')
    ax.set_zlabel('high risk', fontdict={'size': 13, 'color': 'black'})
    ax.set_ylabel('medium risk', fontdict={'size': 13, 'color': 'black'})
    ax.set_xlabel('normal event', fontdict={'size': 13, 'color': 'black'})
    plt.savefig('fig.png', bbox_inches='tight')
    plt.show()

def main():
    documents = read_txt()
    input = []
    for i in documents:
        input = build_matrix(i, input)

    X = np.array(input)
    fuzzy(X)


main()