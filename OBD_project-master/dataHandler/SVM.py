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
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
# Create SVM classification object
from xlwt import Workbook


def svm_test(data):
    # data, label = np.split(data,(13,),axis =1)
    label = np.array(data)[:, -1]
    data = data[:, :-2]
    x_train, x_test, y_train, y_test = skm.train_test_split(data, label, random_state=1,
                                                            train_size=0.8)

    # Create SVM classification object
    # while kernel is linear, the bigger C is, the better performance will be (but may over fitting
    # while kernel is rbf, is gauss kernel, the bigger gamma is, the better performance will be (but may over fitting
    # Penalty parameter C of the error term.
    # gamma: parameter for 'rbf’,'poly' and 'sigmoid'
    # degree: parameter for 'poly'
    # coef0 is a constant for poly
    model = svm.SVC(kernel='poly', C=1, gamma=3,degree = 3,coef0=1)
    model.fit(x_train, y_train.ravel())
    print('train set accuracy:  ', model.score(x_train, y_train.ravel()))
    print('test set accuracy:  ', model.score(x_test, y_test.ravel()))
    plot(data, label, x_test)
    # Predict Output
    # predicted = model.predict(x_test)
    # svm.SVC(C=1.0, kernel='rbf', degree=3, gamma=0.0, coef0=0.0, shrinking=True, probability=False,tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, random_state=None)

    # get accuracy of the model
    # print(clf.score(x_train, y_train))  # 精度
    # y_hat = model.predict(x_train)
    # # show_accuracy(y_hat, y_train, 'train data')
    # print(clf.score(x_test, y_test))


def calcData(data):
    maxAX = max(data[:, 4])
    maxAY = max(data[:, 3])
    minAX = min(data[:, 4])
    minAY = min(data[:, 3])
    rangeAX = maxAX - minAX
    rangeAY = maxAY - minAY
    varAX = np.var(data[:, 4])
    varAY = np.var(data[:, 3])
    varOX = np.var(data[:, 7])
    varOY = np.var(data[:, 6])
    meanAX = np.mean(data[:, 4])
    meanAY = np.mean(data[:, 3])
    meanOX = np.mean(data[:, 7])
    meanOY = np.mean(data[:, 6])
    maxOX = max(data[:, 7])
    maxOY = max(data[:, 6])
    t = data[-1, 1] - data[0, 1]
    meanSP = np.mean(data[:, 3])
    varSP = np.var(data[:, 3])
    return [rangeAX, rangeAY, varAX, varAY, varOX, varOY, meanAX, meanAY, meanOX, meanOY, maxOX,
            maxOY, minAY, meanSP, varSP, t, data[0, -1]]


# load raw data into workspace
def read_excel(file):
    data = xlrd.open_workbook(file)
    table = data.sheets()[0]

    start = 0  # 开始的行
    end = 9767  # 结束的行
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
    for i in range(len(datamatrix)):
        if datamatrix[i, 0] == temp:
            flag += 1
        else:
            vect.append(calcData(datamatrix[i - flag:i, ]))
            temp = datamatrix[i, 0]
            flag = 0
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
    datamatrix = read_excel('svmdata.xls')
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
