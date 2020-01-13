
# from sklearn import svm
from sklearn import svm
import xlrd
import numpy as np
# Create SVM classification object
from xlwt import Workbook
import random
from sklearn.neighbors import NearestNeighbors

def calcData(data):
    maxAX = max(data[:, 4])
    maxAY = max(data[:, 3])
    minAX = min(data[:, 4])
    minAY = min(data[:, 3])
    maxAccX = max(abs(data[:, 4]))
    maxAccY = max(abs(data[:, 3]))
    datalist = data[:, 4].tolist()
    # print(datalist.index(max(datalist)))
    fraction = datalist.index(max(datalist))/len(datalist)
    if(maxAX==maxAccX):
        if(datalist.index(max(datalist))!=0):
            firstHalfMean = np.mean(data[0:datalist.index(max(datalist)),4])
        else:
            firstHalfMean = datalist[0];

    else:
        if (datalist.index(min(datalist)) != 0):
            firstHalfMean = np.mean(data[0:datalist.index(min(datalist)),4])
        else:
            firstHalfMean = datalist[0];


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
    maxOri = max(maxOX,maxOY)
    t = (data[-1, 1] - data[0, 1])/1000
    meanSP = np.mean(data[:, 2])
    varSP = np.std(data[:, 2])
    differenceSP = data[-1, 2]-data[0, 2]
    accelerate = differenceSP / t
    StartEndAccx = data[0,4]+data[-1,4]
    StartEndAccy = data[0,3]+data[-1,3]
    # return [rangeAX, rangeAY, varAX, varAY, varOX, maxOri, maxAX, minAX, maxAccY, differenceSP, t, data[0, -1]]  #92% 78% 去掉平均
    # return [rangeAX, rangeAY, meanAX, meanAY, meanOX, maxOri, maxAX, minAX, maxAccY, differenceSP, t, data[0, -1]]  #93% 85% 去掉std
    # return [ varAX, varAY, varOX, meanAX, meanAY, meanOX, maxOri, maxAX, minAX, maxAccY, differenceSP, t, data[0, -1]]  #92% 83% 去掉范围
    # return [rangeAX, rangeAY, varAX, varAY, varOX, meanAX, meanAY, meanOX, maxOri, maxAX, minAX, maxAccY, differenceSP, t, data[0, -1]]  #95% 85%
    # return [rangeAX, rangeAY, varAX, varAY, varOX, meanAX, meanAY, meanOX, maxOri, maxAX, maxAY, minAX, minAY, differenceSP, t, data[0, -1]]  #96% 83%
    # return [rangeAX, rangeAY, varAX, varAY, varOX, meanAX, meanAY,meanOX, maxOX, maxAX,maxAY, minAX, minAY, accelerate, meanSP, t, data[0, -1]] #97% 85%
    # return [rangeAX, rangeAY, varAX, varAY, varOX, meanAX, meanAY,meanOX, maxOX, maxAX,maxAY, minAX, minAY, differenceSP, meanSP, t, data[0, -1]] #97% 85%
    return [rangeAX, rangeAY, varAX, varAY, meanAX, meanAY, meanOX, maxOri, maxAX, maxAY, minAX, minAY, differenceSP, meanSP,StartEndAccx,StartEndAccy, t, data[0, -1]] #99% 86%
    # return [rangeAX, rangeAY, varAX, varAY, varOX, meanAX, meanAY, meanOX, maxOri, maxAX, maxAY, minAX, minAY, differenceSP, meanSP, t, data[0, -1]] #96% 86%
    # return [rangeAX, rangeAY, varAX, varAY, varOX, meanAX, meanAY, meanOX, maxOri, maxAX, maxAY, minAX, minAY, differenceSP, meanSP, varSP, t, data[0, -1]] #97.5% 83%
    # return [rangeAX, rangeAY, varAX, varAY, varOX, varOY, meanAX, meanAY, meanOX, meanOY, maxOri, maxAX, maxAY, minAX, minAY, differenceSP, meanSP, varSP, t, data[0, -1]] #98% 83%

# load raw data into workspace
def read_excel(file):
    data = xlrd.open_workbook(file)
    table = data.sheets()[0]

    start = 0  # 开始的行
    end = 23284 # 结束的行

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
    # file_w = Workbook()
    # table = file_w.add_sheet(u'Data', cell_overwrite_ok=True)  # 创建sheet
    # write_data(np.array(resultMatrix), table)
    # file_w.save('ForLDA.xls')

    # linear normalization
    max = np.max(vect, axis=0)
    min = np.min(vect, axis=0)
    # max = [0.7614, 0.6011, 0.2729, 0.2104, 11.510, 4.6303, 0.2529, 0.2861, 13.922, 1.6740, 31.65, 0.51791, 0.54475,
    #        0.1544,
    #        0.0674, 75.0, 94.7125, 29.1634,17.16]
    # min = [0.06909, 0.0079, 0.0206, 0.0020, 0.3709, 0.7642, -0.356, -0.277, -16.325, -2.0252, 2.27, -0.0867, -0.0405,
    #        -0.748,
    #        -0.589, -90.0, 2.67796, 0.40508, 1.848]
    for i in range(len(vect[0])-1):
        # print(max[i])
        # print(min[i])
        for j in range(len(vect)):
            # if(i==12):
            #     vect[j][i] = ((vect[j][i]-min[i])/(max[i]-min[i])*2)-1
            # else:
                vect[j][i] = (vect[j][i]-min[i])/(max[i]-min[i])


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

class Smote:
    def __init__(self, samples, N=10, k=5):
        self.n_samples, self.n_attrs = samples.shape
        self.N = N
        self.k = k
        self.samples = samples
        self.newindex = 0

    def over_sampling(self):
        N = int(self.N / 100)
        self.synthetic = np.zeros((self.n_samples * N, self.n_attrs))
        neighbors = NearestNeighbors(n_neighbors=self.k).fit(self.samples)
        # print('neighbors', neighbors)
        for i in range(len(self.samples)):
            print('samples', self.samples[i])
            nnarray = neighbors.kneighbors(self.samples[i].reshape((1, -1)), return_distance=False)[
                0]  # Finds the K-neighbors of a point.
            print('nna', nnarray)
            self._populate(N, i, nnarray)
        return self.synthetic

    def _populate(self, N, i, nnarray):
        for j in range(N):
            # print('j', j)
            nn = random.randint(0, self.k - 1)  # 包括end
            dif = self.samples[nnarray[nn]] - self.samples[i]
            gap = random.random()
            self.synthetic[self.newindex] = self.samples[i] + gap * dif
            self.newindex += 1
            # print(self.newindex)

def read_excel2():
    data = xlrd.open_workbook('Smote.xlsx')
    table = data.sheets()[0]

    start = 0  # 开始的行
    end = 6 # 结束的行
    # end = 6847  # 结束的行
    rows = end - start

    list_values = []
    for x in range(start, end):
        values = []
        row = table.row_values(x)
        # all data from excel
        for i in range(19):
            # print(value)
            values.append(row[i])
        list_values.append(values)
    datamatrix = np.array(list_values)
    datamatrix = datamatrix.astype(np.float64)
    # print(datamatrix)
    return datamatrix

def main():
    datamatrix = read_excel('label data.xlsx')
    vect = np.array(init(datamatrix))
    print(vect)
    write_excel(vect, 'vect.xls')

    # a = read_excel2()
    # s = Smote(a, N=100)
    # oversampling = s.over_sampling()
    # print(oversampling)
    # write_excel(oversampling,'SmoteOutput.xls')


if __name__ == "__main__":
    main()