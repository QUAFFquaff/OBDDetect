import joblib
from sklearn import svm
import xlrd
import numpy as np

svm = joblib.load('svm.pkl')


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
            maxOY, maxAX, maxAY, minAX, minAY, differenceSP, maxSP, meanSP, varSP, t]

# load raw data into workspace
def read_excel(file):
    data = xlrd.open_workbook(file)
    table = data.sheets()[0]

    start = 0  # 开始的行
    end = 125 # 结束的行
    # end = 6847  # 结束的行
    rows = end - start

    list_values = []
    for x in range(start, end):
        values = []
        row = table.row_values(x)
        # all data from excel
        for i in range(9):
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

    # linear normalization
    # max = np.max(vect, axis=0)
    # min = np.min(vect, axis=0)
    max = [0.619, 0.944, 0.546, 0.418, 0.208, 0.281, 6.075, 17.258, 0.286, 0.349, 3.901, 26.569, 22.12, 60.271,
           0.594,
           0.932, 0.097, 0.191, 90, 136,
           122.637, 29.291, 24.982]
    min = [0.034, 0.021, -0.302, -0.249, 0.009, 0.004, 0.325, 0.575, -0.312, -0.281, -3.816, -20.210, -0.061,
           -1.291,
           -0.063, -0.067, -0.539, -0.818, -76, 5,
           4.979, 0.408, 1.581]
    for i in range(len(vect[0])):
        # print(max[i])
        # print(min[i])
        for j in range(len(vect)):
            vect[j][i] = (vect[j][i]-min[i])/(max[i]-min[i])
            #vect[j][i] = atan(vect[j][i])*2/pi
    return vect

def main():
    datamatrix = read_excel('labeldata.xlsx')
    vect = np.array(init(datamatrix))
    print(vect)
    result = svm.predict(vect)
    print(result)
    score = svm.decision_function(vect)
    print(score)


if __name__ == "__main__":
    main()