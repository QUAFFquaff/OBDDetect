#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 1/20/2020 0:04
# @Author  : Haoyu Lyu
# @File    : fuzzy_c.py
# @Software: PyCharm

from fcmeans import FCM
from sklearn.datasets import make_blobs
from matplotlib import pyplot as plt
from seaborn import scatterplot as scatter
import numpy as np

# create artifitial dataset
# n_samples = 50000
# n_bins = 3  # use 3 bins for calibration_curve as we have 3 clusters here
# centers = [(-5, -5), (0, 0), (5, 5)]
#
# X,_ = make_blobs(n_samples=n_samples, n_features=2, cluster_std=1.0,
#                   centers=centers, shuffle=False, random_state=42)

X = np.array([(1,1),(1,2),(1,3),(2,2),(10,10),(100,100),(101,101),(102,102)])
# print(X.type)
# fit the fuzzy-c-means
fcm = FCM(n_clusters=2)
fcm.fit(X)

# outputs
fcm_centers = fcm.centers
fcm_labels  = fcm.u.argmax(axis=1)


# plot result
# %matplotlib inline
f, axes = plt.subplots(1, 2, figsize=(11,5))
scatter(X[:,0], X[:,1], ax=axes[0])
scatter(X[:,0], X[:,1], ax=axes[1], hue=fcm_labels)
scatter(fcm_centers[:,0], fcm_centers[:,1], ax=axes[1],marker="s",s=200)
plt.show()