
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
from sklearn.metrics import silhouette_score
import xlrd
import numpy as np


# data=[[0.404120557,0,1,0,0],
#       [0.512964448,0,1,0,0],
#       [0.496052632,0,1,0,0],
#       [0.376337948,0.301478953,0.481481481,0.185185185,0.333333333],
#       [0.659807956,0.408969409,0.393939394,0.151515152,0.454545455],
#       [0.355084799,0.169566761,0.608695652,0.239130435,0.152173913],
#       [0.417582103,0.043360914,0.862745098,0.098039216,0.039215686],
#       [0.485730362,0.072690972,0.848484848,0.060606061,0.090909091],
#       [0.540712152,0,0.933333333,0.066666667,0],
#       [0.386690602,0,1,0,0]]
Data=[]
data = xlrd.open_workbook('KMeansData.xlsx')
table = data.sheet_by_index(0)
for i in range(0,table.nrows):
    Data.append(table.row_values(i))
Data = np.array(Data)
Data = Data.astype(np.float64)

print(Data)

# this is the elbow method
SSE = []  # sum of the squared errors
# num_clusters = 2
for num_clusters in range(1,9):
    km_cluster = KMeans(n_clusters=num_clusters, max_iter=300, n_init=40, init='k-means++',n_jobs=-1)
    km_cluster.fit(Data)
    SSE.append(km_cluster.inertia_)
X = range(1,9)
plt.xlabel('k')
plt.ylabel('SSE')
plt.plot(X,SSE,'o-')
plt.show()
# labels = km_cluster.labels_
# center = km_cluster.cluster_centers_
# predict = km_cluster.predict(data)
# print(labels)
# print(center)
# print(predict)


# this is the Average silhouette method
Scores = []
for num_clusters in range(2,9):
    km_cluster = KMeans(n_clusters=num_clusters, max_iter=300, n_init=40, init='k-means++', n_jobs=-1)
    km_cluster.fit(Data)
    Scores.append(silhouette_score(Data,km_cluster.labels_,metric='euclidean'))
X = range(2,9)
plt.xlabel('k')
plt.ylabel('average silhouette width ')
plt.plot(X,Scores,'o-')
plt.show()