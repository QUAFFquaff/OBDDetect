#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 1/19/2020 23:42
# @Author  : Haoyu Lyu
# @File    : fuzzy.py
# @Software: PyCharm

from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt

class Data(object):
    def __init__(self):
        pass

    def generate(self):
        self.colors = ['b', 'orange', 'g', 'r', 'c', 'm', 'y', 'k', 'Brown', 'ForestGreen']

        # Define three cluster centers
        centers = [[4, 2],
                [1, 7],
                [5, 6]]

        # Define three cluster sigmas in x and y, respectively
        sigmas = [[0.8, 0.3],
                [0.3, 0.5],
                [1.1, 0.7]]

        # Generate test data
        np.random.seed(42)  # Set seed for reproducibility
        self.xpts = np.zeros(1)
        self.ypts = np.zeros(1)
        self.labels = np.zeros(1)

        # 伪造3个高斯分布，以u和sigma作为特征分布
        for i, ((xmu, ymu), (xsigma, ysigma)) in enumerate(zip(centers, sigmas)):
            self.xpts = np.hstack((self.xpts, np.random.standard_normal(200) * xsigma + xmu))
            self.ypts = np.hstack((self.ypts, np.random.standard_normal(200) * ysigma + ymu))
            self.labels = np.hstack((self.labels, np.ones(200) * i))
        return self.xpts, self.ypts, self.labels

    def visualize(self):
        # Visualize the test data
        fig0, ax0 = plt.subplots()
        for label in range(3):
            ax0.plot(self.xpts[self.labels == label], self.ypts[self.labels == label], '.',
                    color=self.colors[label])
        ax0.set_title('Test data: 200 points x3 clusters.')
        # plt.show()

class Fuzzy(object):
    def __init__(self, xpts, ypts, labels):
        self.xpts = xpts
        self.ypts = ypts
        self.labels = labels

    def _norm1(self, array):
        array = np.abs(array)
        return np.sum(array)

    def _normalize_rows(self, rows):
        normalized_rows = rows / np.sum(rows, axis=1, keepdims=1)
        return normalized_rows

    def cluster(self, classes, m = 2, niter = 1000, error = 1e-5):

        # init u
        # u = np.ones([len(self.labels), classes], dtype=np.float32) / 3
        n_data = self.xpts.shape[0]
        u = np.random.rand(n_data, classes)
        u = self._normalize_rows(u)

        self.x = np.array(zip(self.xpts, self.ypts))

        len_j = u.shape[1]
        c = np.zeros([len_j, 2], dtype=np.float32)

        for n in range(niter):
            # calculate c_j
            for j in range(len_j):
                u_j = u[:, j]
                u_jm = u_j ** m
                numer = np.dot(u_jm, self.x)
                deno = np.sum(u_jm)
                c[j] = numer / deno

            # update u_k
            u_new = np.zeros_like(u)
            data_size = self.x.shape[0]
            class_size = c.shape[0]
            for i in range(data_size):
                for j in range(class_size):
                    numer = 0
                    for k in range(c.shape[0]):
                        temp = self._norm1(self.x[i] - c[j]) / self._norm1(self.x[i] - c[k])
                        temp = temp ** (2 / (m-1))
                        numer += temp
                    u_new[i, j] = 1 / numer

            # check convergence
            print('FCM steps:', n)
            if(self._norm1(u - u_new) < error):
                break

            # update u
            u = u_new

        # return value and center
        predict = np.argmax(u, axis=1)
        return c, predict

if __name__ == '__main__':
    # generate data
    data = Data()
    xpts, ypts, labels = data.generate()
    data.visualize()

    # fuzzy c means
    fuzzy = Fuzzy(xpts, ypts, labels)
    center, predict_labels = fuzzy.cluster(classes=3, m=2, niter = 1000)

    # visualize
    colors = ['b', 'orange', 'g', 'r', 'c', 'm', 'y', 'k', 'Brown', 'ForestGreen']
    fig, ax = plt.subplots()
    for i in range(3):
        ax.plot(xpts[predict_labels == i],
                ypts[predict_labels == i],
                '.',
                color=colors[i])
    for pt in center:
        ax.plot(pt[0], pt[1], 'rs')
    ax.set_title('clustering results')
    plt.show()