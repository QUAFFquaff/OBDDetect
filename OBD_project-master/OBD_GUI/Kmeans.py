
'''

@author: Daben

@contact: dabenw@uci.edu

@file: Kmeans.py

@time: 2019/4/19

@desc: k-means cluster

'''

from numpy import *
import time
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


data=[[0.404120557,0,1,0,0],
      [0.512964448,0,1,0,0],
      [0.496052632,0,1,0,0],
      [0.376337948,0.301478953,0.481481481,0.185185185,0.333333333],
      [0.659807956,0.408969409,0.393939394,0.151515152,0.454545455],
      [0.355084799,0.169566761,0.608695652,0.239130435,0.152173913],
      [0.417582103,0.043360914,0.862745098,0.098039216,0.039215686],
      [0.485730362,0.072690972,0.848484848,0.060606061,0.090909091],
      [0.540712152,0,0.933333333,0.066666667,0],
      [0.386690602,0,1,0,0]]

num_clusters = 2
km_cluster = KMeans(n_clusters=num_clusters, max_iter=300, n_init=40, init='k-means++',n_jobs=-1)
km_cluster.fit(data)
labels = km_cluster.labels_
center = km_cluster.cluster_centers_
predict = km_cluster.predict(data)
print(labels)
print(center)
print(predict)

