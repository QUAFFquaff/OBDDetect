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
    end = 328 # 结束的行
    # end = 6847  # 结束的行
    rows = end - start

    list_values = []
    for x in range(start, end):
        values = []
        row = table.row_values(x)
        # all data from excel
        if(x==number-1):
            for i in range(24):
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
    #model = svm.SVC(kernel='poly', C=1, gamma=3,degree = 2,coef0=1, probability=True, class_weight='balanced')
    #model = svm.SVC(kernel='rbf', C=2, gamma=2, degree=3, coef0=0.0, shrinking=True, max_iter=-1, probability=True, decision_function_shape='ovr')
    model = svm.SVC(kernel='rbf', C=5, gamma=5, degree=3, coef0=0.0, shrinking=True, max_iter=-1, probability=True, class_weight='balanced')
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

    for i in range(1,328):
        predict = read_excel1(i)
        y_hat = model.predict(predict[:,:23])
        y_pro = model.predict_proba(predict[:,:23])
        y_score = model.decision_function(predict[:,:23])
        if(y_hat!=predict[:,-1]):
            print("prob", y_pro)
            print("score", y_score)
            print("predict as",y_hat)
            print("but graound truth is ",predict[:,-1])
            print(predict[:,-2])
            print('*****************')

    # # show_accuracy(y_hat, y_train, 'train data')
    # print(clf.score(x_test, y_test))


def calcData(data):
    maxAX = max(data[:, 4])
    maxAY = max(data[:, 3])
    minAX = min(data[:, 4])
    minAY = min(data[:, 3])
    rangeAX = maxAX - minAX
    rangeAY = maxAY - minAY
    startAY = data[0, 3]
    endAY = data[-1, 3]
    varAX = np.std(data[:, 4])
    varAY = np.std(data[:, 3])
    varOX = np.std(data[:, 7])
    varOY = np.std(data[:, 6])
    meanAX = np.mean(data[:, 4])
    meanAY = np.mean(data[:, 3])
    meanOX = np.mean(data[:, 7])
    meanOY = np.mean(data[:, 6])
    maxOX = max(abs(data[:, 7]))
    maxOY = max(abs(data[:, 6]))
    t = (data[-1, 1] - data[0, 1])/1000
    maxSP = max(data[:, 2])
    meanSP = np.mean(data[:, 2])
    varSP = np.std(data[:, 2])
    differenceSP = data[-1, 2]-data[0, 2]
    return [rangeAX, rangeAY, startAY, endAY, varAX, varAY, varOX, varOY, meanAX, meanAY, meanOX, meanOY, maxOX,
            maxOY, maxAX, maxAY, minAX, minAY, differenceSP, maxSP, meanSP, varSP, t, data[0, -1]]


# load raw data into workspace
def read_excel(file):
    data = xlrd.open_workbook(file)
    table = data.sheets()[0]

    start = 0  # 开始的行
    end = 13419 # 结束的行
    # end = 6847  # 结束的行
    rows = end - start

    list_values = []
    for x in range(start, end):
        values = []
        row = table.row_values(x)
        # all data from excel
        for i in range(10):
            # print(value)
            values.append(row[i])
        list_values.append(values)
    # print(list_values)
    datamatrix = np.array(list_values)
    datamatrix = datamatrix.astype(np.float64)
    # print(datamatrix)
    return datamatrix




# split data by event
def init(datamatrix):
    datamatrix = np.array(datamatrix)
    temp = 1.0
    vect = []  # break labeled 1
    speedV = []  # speed up labeled 2
    flag = 0
    resultMatrix = []
    for i in range(len(datamatrix)):
        if datamatrix[i, 0] == temp:
            flag += 1
        else:
            vect.append(calcData(datamatrix[i - flag:i, ]))
            resultMatrix.append([datamatrix[i-flag,1],datamatrix[i-1,1],datamatrix[i-1,-1]])
            temp = datamatrix[i, 0]
            flag = 1
    vect.append(calcData(datamatrix[len(datamatrix)+1 - flag:len(datamatrix)+1, ]))
    file_w = Workbook()
    table = file_w.add_sheet(u'Data', cell_overwrite_ok=True)  # 创建sheet
    write_data(np.array(resultMatrix), table)
    file_w.save('ForLDA.xls')

    # linear normalization
    max = np.max(vect, axis=0)
    min = np.min(vect, axis=0)
    for i in range(len(vect[0])-1):
        # print(max[i])
        # print(min[i])
        for j in range(len(vect)):
            vect[j][i] = (vect[j][i]-min[i])/(max[i]-min[i])
            #vect[j][i] = atan(vect[j][i])*2/pi
    return vect


def write_data(dataTemp, table):
    data = np.array(dataTemp)
    [h, l] = data.shape  # h为行数，l为列数
    for i in range(h):
        for j in range(l):
            table.write(i, j, data[i][j])


def write_excel(data, file_name):
    file_w = Workbook()
    table = file_w.add_sheet(u'Data', cell_overwrite_ok=True)  # 创建sheet
    write_data(data, table)
    file_w.save(file_name)


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
    datamatrix = read_excel('label data.xlsx')
    vect = np.array(init(datamatrix))
    write_excel(vect, 'vect.xls')
    # x = vect[:,0:-2]
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
