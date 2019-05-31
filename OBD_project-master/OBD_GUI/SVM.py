#!/usr/bin/env python

# encoding: utf-8

'''

@author: Quaff

@contact: Quaff.lyu@gmail.com

@file: SVM.py

@time: 2019/2/14 19:37

@desc:

'''

# from sklearn import svm
from sklearn import svm
import xlrd
import sklearn.model_selection as skm
from sklearn.multiclass import OneVsOneClassifier
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
# Create SVM classification object
from xlwt import Workbook
from math import *
from sklearn.externals import joblib

def read_excel1(number):
    data = xlrd.open_workbook('vect.xls')
    table = data.sheets()[0]

    start = 0  # 开始的行
    end = 198 # 结束的行
    # end = 6847  # 结束的行
    rows = end - start

    list_values = []
    for x in range(start, end):
        values = []
        row = table.row_values(x)
        # all data from excel
        if(x==number-1):
            for i in range(20):
                # print(value)
                values.append(row[i])
            list_values.append(values)
    # print(list_values)
    datamatrix = np.array(list_values)
    datamatrix = datamatrix.astype(np.float64)
    # print(datamatrix)
    return datamatrix

def svm_test(data):
    # data, label = np.split(data,(13,),axis =1)
    label = np.array(data)[:, -1]
    data = data[:, :-1]
    label.astype(int)
    x_train, x_test, y_train, y_test = skm.train_test_split(data, label, random_state=1,
                                                            train_size=0.8)
    # x_train = data[:100,:]
    # y_train = label[:100]
    # x_test = data[100:106,:]
    # y_test = label[100:106]
    # Create SVM classification object
    # while kernel is linear, the bigger C is, the better performance will be (but may over fitting
    # while kernel is rbf, is gauss kernel, the bigger gamma is, the better performance will be (but may over fitting
    # Penalty parameter C of the error term.
    # gamma: parameter for 'rbf’,'poly' and 'sigmoid'
    # degree: parameter for 'poly'
    # coef0 is a constant for poly
    #model = svm.SVC(kernel='poly', C=1, gamma=3,degree = 4,coef0=1, probability=True, class_weight='balanced')
    #model = svm.SVC(kernel='rbf', C=2, gamma=2, degree=3, coef0=0.0, shrinking=True, max_iter=-1, probability=True, decision_function_shape='ovr')
    model = svm.SVC(kernel='rbf', C=4, gamma=5, degree=3, coef0=0.0, shrinking=True, max_iter=-1, probability=True, class_weight='balanced')
    model.fit(x_train, y_train.ravel())

    print('train set accuracy:  ', model.score(x_train, y_train.ravel()))
    print('test set accuracy:  ', model.score(x_test, y_test.ravel()))

    joblib.dump(model, 'svm.pkl')
    # plot(data, label, x_test)
    # Predict Output
    # predicted = model.predict(x_test)
    # svm.SVC(C=1.0, kernel='rbf', degree=3, gamma=0.0, coef0=0.0, shrinking=True, probability=False,tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, random_state=None)

    # get accuracy of the model
    # print(clf.score(x_train, y_train))  # 精度

    for i in range(1,198):
        predict = read_excel1(i)
        y_hat = model.predict(predict[:,:19])
        y_pro = model.predict_proba(predict[:,:19])
        y_score = model.decision_function(predict[:,:19])
        if(y_hat!=predict[:,-1]):
            # print("prob", y_pro)
            print(predict[:,:19])
            print("score", y_score)
            y_score = np.array(y_score[0])
            print("predict as",y_hat)
            print("but graound truth is ",predict[:,-1])
            print(predict[:,-2])
            print('*****************')

    # # show_accuracy(y_hat, y_train, 'train data')
    # print(clf.score(x_test, y_test))




def read_excel2():
    data = xlrd.open_workbook('vect.xls')
    table = data.sheets()[0]

    start = 0  # 开始的行
    end = 198 # 结束的行
    # end = 6847  # 结束的行
    rows = end - start

    list_values = []
    for x in range(start, end):
        values = []
        row = table.row_values(x)
        # all data from excel
        for i in range(20):
            # print(value)
            values.append(row[i])
        list_values.append(values)
    datamatrix = np.array(list_values)
    datamatrix = datamatrix.astype(np.float64)
    # print(datamatrix)
    return datamatrix


def plot(x, y, x_test):
    colm1 = 6
    colm2 = 10
    x1_min, x1_max = x[:, colm1].min(), x[:, colm1].max()  # 第0列的范围
    x2_min, x2_max = x[:, colm2].min(), x[:, colm2].max()  # 第1列的范围
    x1, x2 = np.mgrid[x1_min:x1_max:200j, x2_min:x2_max:200j]  # 生成网格采样点
    grid_test = np.stack((x1.flat, x2.flat), axis=1)  # 测试点
    # print 'grid_test = \n', grid_testgrid_hat = clf.predict(grid_test)       # 预测分类值grid_hat = grid_hat.reshape(x1.shape)  # 使之与输入的形状相同

    # font
    mpl.rcParams['font.sans-serif'] = [u'SimHei']
    mpl.rcParams['axes.unicode_minus'] = False

    # draw the plot
    cm_light = mpl.colors.ListedColormap(['#A0FFA0', '#FFA0A0', '#A0A0FF'])
    cm_dark = mpl.colors.ListedColormap(['g', 'r', 'b'])
    # plt.pcolormesh(x1, x2, grid_test, cmap=cm_light)
    plt.scatter(x[:, colm1], x[:, colm2], c=y, edgecolors='k', s=50, cmap=cm_dark)  # 样本
    plt.scatter(x_test[:, colm1], x_test[:, colm2], s=120, facecolors='none', zorder=10)  # 圈中测试集样本
    plt.xlabel(u'meanAX', fontsize=13)
    plt.ylabel(u'maxOX', fontsize=13)
    plt.xlim(x1_min, x1_max)
    plt.ylim(x2_min, x2_max)
    plt.title(u'SpeedUp & Break & turn', fontsize=15)
    # plt.grid()
    plt.show()
    pass


def main():
    vect = read_excel2()
    svm_test(vect)


if __name__ == "__main__":
    main()







# model = svm.svc(kernel="linear", c=1, gamma=1)
# # Create SVM classification object
# model = svm.svc(kernel='linear', c=1, gamma=1)
# # there is various option associated with it, like changing kernel, gamma and C value. Will discuss more # about it in next section.Train the model using the training sets and check score
# model.fit(X, y)
# model.score(X, y)
# # Predict Output
# predicted = model.predict(x_test)
# # svm.SVC(C=1.0, kernel='rbf', degree=3, gamma=0.0, coef0=0.0, shrinking=True, probability=False,tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, random_state=None)
