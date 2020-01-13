
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
from mpl_toolkits.mplot3d import Axes3D
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
# data = xlrd.open_workbook('KMeansData.xlsx')
data = xlrd.open_workbook('ForKMeans.xls')
table = data.sheet_by_index(0)
for i in range(0,table.nrows):
    Data.append(table.row_values(i))
Data = np.array(Data)
Data = Data.astype(np.float64)

# print(Data)


km_cluster = KMeans(n_clusters=4, max_iter=300, n_init=40, init='k-means++',n_jobs=-1)
km_cluster.fit(Data)
labels = km_cluster.labels_
cluster0 =Data[(km_cluster.labels_==0)]
cluster1 =Data[(km_cluster.labels_==1)]
cluster2 =Data[(km_cluster.labels_==2)]
cluster3 =Data[(km_cluster.labels_==3)]
print(labels)
print("-----")
centers = km_cluster.cluster_centers_
# print(centers)
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(cluster0[:,2],cluster0[:,3],cluster0[:,5],c='r',label='first cluster')
ax.scatter(cluster1[:,2],cluster1[:,3],cluster1[:,5],c='b',label='second cluster')
ax.scatter(cluster2[:,2],cluster2[:,3],cluster2[:,5],c='g',label='third cluster')
ax.scatter(cluster3[:,2],cluster3[:,3],cluster3[:,5],c='y',label='fourth cluster')
print(len(cluster0))
print(cluster0[0])
ax.scatter(centers[0][2],centers[0][3],centers[0][5],marker='*',c='r')
ax.scatter(centers[1][2],centers[1][3],centers[1][5],marker='1',c='b')
ax.scatter(centers[2][2],centers[2][3],centers[2][5],marker='P',c='g')
ax.scatter(centers[3][2],centers[3][3],centers[3][5],marker='x',c='y')

ax.legend(loc='best')

ax.set_zlabel('angry pattern', fontdict={'size': 13, 'color': 'black'})
ax.set_ylabel('low scores pattern percent', fontdict={'size': 13, 'color': 'black'})
ax.set_xlabel('high risk frequency', fontdict={'size': 13, 'color': 'black'})
plt.savefig("distribution1.png")
plt.show()


# # using MDS method
# from sklearn.manifold import MDS
# clf = MDS(3)
# clf.fit(Data)
# personData = clf.fit_transform(Data)
# plt.scatter(personData[:,0],personData[:,1],c =km_cluster.labels_)
# # fig = plt.figure()
# # ax = Axes3D(fig)
# # ax.scatter(personData[:,0],personData[:,1], personData[:,2],c =km_cluster.labels_)
# # ax.legend(loc='best')
# plt.title('Using sklearn MDS in 3d')
# plt.savefig("MDS_2d.png")
# plt.show()


from sklearn.metrics.pairwise import euclidean_distances

# this is the elbow method
SSE = []  # sum of the squared errors
interDis = []
# num_clusters = 2
for num_clusters in range(2,7):
    km_cluster = KMeans(n_clusters=num_clusters, max_iter=300, n_init=10, init='k-means++',n_jobs=-1)
    km_cluster.fit(Data)
    SSE.append(km_cluster.inertia_)

    dist = euclidean_distances(km_cluster.cluster_centers_)
    tri_dists = dist[np.triu_indices(num_clusters, 1)]

    dis_inertia = []
    for i in range(num_clusters):
        distance = []
        for point in range(len(Data[(km_cluster.labels_==i)])):
            distance.append(euclidean_distances([Data[(km_cluster.labels_==i)][point],km_cluster.cluster_centers_[i]])[0][1])
        dis_inertia.append(max(distance))

    dunIndex = tri_dists.min() /max(dis_inertia)
    print(tri_dists.min())
    # print(tri_dists.max())
    print(tri_dists.mean())
    interDis.append(dunIndex)
print(SSE)
X = range(2,7)
plt.xlabel('number of clusters')
plt.ylabel('SSE(Sum Of the  intra cluster distance)')
plt.plot(X,SSE,'o-')
plt.savefig("elbowMethod.png")
plt.show()
# labels = km_cluster.labels_
center = km_cluster.cluster_centers_
# predict = km_cluster.predict(data)
# print(labels)
# print(center)
# print(predict)
# X = range(2,8)
# plt.xlabel('number of clusters')
# plt.ylabel('inter distance ')
# plt.plot(X,interDis,'o-')
# plt.savefig("elbowMethod2.png")
# plt.show()



# # this is the Average silhouette method
# Scores = []
# for num_clusters in range(2,6):
#     km_cluster = KMeans(n_clusters=num_clusters, max_iter=300, n_init=40, init='k-means++', n_jobs=-1)
#     km_cluster.fit(Data)
#     Scores.append(silhouette_score(Data,km_cluster.labels_,metric='euclidean'))
# X = range(2,6)
# plt.xlabel('number of clusters')
# plt.ylabel('average silhouette width ')
# plt.plot(X,Scores,'o-')
# plt.savefig("silhouetteMethod.png")
# plt.show()
