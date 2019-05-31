import joblib
from sklearn import svm
import xlrd
import numpy as np
from scipy import signal

# svm = joblib.load('svm.pkl')
#
#
# def calcData(data):
#     maxAX = max(data[:, 4])
#     maxAY = max(data[:, 3])
#     minAX = min(data[:, 4])
#     minAY = min(data[:, 3])
#     rangeAX = maxAX - minAX
#     rangeAY = maxAY - minAY
#     startAY = data[0, 3]
#     endAY = data[-1, 3]
#     varAX = np.std(data[:, 4])
#     varAY = np.std(data[:, 3])
#     varOX = np.std(data[:, 7])
#     varOY = np.std(data[:, 6])
#     meanAX = np.mean(data[:, 4])
#     meanAY = np.mean(data[:, 3])
#     meanOX = np.mean(data[:, 7])
#     meanOY = np.mean(data[:, 6])
#     maxOX = max(abs(data[:, 7]))
#     maxOY = max(abs(data[:, 6]))
#     maxOri = max(maxOX, maxOY)
#     t = (data[-1, 1] - data[0, 1])/1000
#     maxSP = max(data[:, 2])
#     meanSP = np.mean(data[:, 2])
#     varSP = np.std(data[:, 2])
#     differenceSP = data[-1, 2]-data[0, 2]
#     return [rangeAX, rangeAY,varAX, varAY, varOX, varOY, meanAX, meanAY, meanOX, meanOY,maxOri, maxAX, maxAY, minAX, minAY, differenceSP, meanSP, varSP, t]
#
# # load raw data into workspace
# def read_excel(file):
#     data = xlrd.open_workbook(file)
#     table = data.sheets()[0]
#
#     start = 0  # 开始的行
#     end = 63 # 结束的行
#     # end = 6847  # 结束的行
#     rows = end - start
#
#     list_values = []
#     for x in range(start, end):
#         values = []
#         row = table.row_values(x)
#         # all data from excel
#         for i in range(9):
#             # print(value)
#             values.append(row[i])
#         list_values.append(values)
#     # print(list_values)
#     datamatrix = np.array(list_values)
#     datamatrix = datamatrix.astype(np.float64)
#     # print(datamatrix)
#     return datamatrix
#
# # split data by event
# def init(datamatrix):
#     datamatrix = np.array(datamatrix)
#     temp = 1.0
#     vect = []  # break labeled 1
#     speedV = []  # speed up labeled 2
#     flag = 0
#     resultMatrix = []
#     for i in range(len(datamatrix)):
#         if datamatrix[i, 0] == temp:
#             flag += 1
#         else:
#             vect.append(calcData(datamatrix[i - flag:i, ]))
#             resultMatrix.append([datamatrix[i-flag,1],datamatrix[i-1,1],datamatrix[i-1,-1]])
#             temp = datamatrix[i, 0]
#             flag = 1
#     vect.append(calcData(datamatrix[len(datamatrix)+1 - flag:len(datamatrix)+1, ]))
#
#     # linear normalization
#     # max = np.max(vect, axis=0)
#     # min = np.min(vect, axis=0)
#     max = [0.7614, 0.6011, 0.2729, 0.2104, 11.510, 4.6303, 0.2529, 0.2861, 13.922, 1.6740, 31.65, 0.51791, 0.54475,
#            0.1544,
#            0.0674, 75.0, 94.7125, 29.1634,17.16]
#     min = [0.06909, 0.0079, 0.0206, 0.0020, 0.3709, 0.7642, -0.356, -0.277, -16.325, -2.0252, 2.27, -0.0867, -0.0405,
#            -0.748,
#            -0.589, -90.0, 2.67796, 0.40508, 1.848]
#     for i in range(len(vect[0])):
#         # print(max[i])
#         # print(min[i])
#         for j in range(len(vect)):
#             vect[j][i] = (vect[j][i]-min[i])/(max[i]-min[i])
#             #vect[j][i] = atan(vect[j][i])*2/pi
#     return vect
#
# def main():
#     datamatrix = read_excel('labeldata.xlsx')
#     vect = np.array(init(datamatrix))
#     print(vect)
#     result = svm.predict(vect)
#     print(result)
#     score = svm.decision_function(vect)
#     print(score)
#     prob = svm.predict_proba(vect)
#     print(prob)
#
#
# if __name__ == "__main__":
#     main()


n= []
m=[]
m.append(1)
m.append(2)
m.append(3)
n.append(m)
m=[]
m.append(4)
m.append(5)
m.append(6)
n.append(m)
m=[]
m.append(7)
m.append(8)
m.append(9)
n.append(m)
m=[]
m.append(7)
m.append(8)
m.append(9)
n.append(m)
m=[]
m.append(7)
m.append(8)
m.append(9)
n.append(m)
m=[]
m.append(7)
m.append(8)
m.append(9)
n.append(m)
m=[]
m.append(7)
m.append(8)
m.append(9)
n.append(m)
m=[]
m.append(7)
m.append(8)
m.append(9)
n.append(m)
m=[]
m.append(7)
m.append(8)
m.append(9)
n.append(m)
m=[]
m.append(7)
m.append(8)
m.append(9)
n.append(m)
m=[]
m.append(7)
m.append(8)
m.append(9)
n.append(m)
m=[]
m.append(7)
m.append(8)
m.append(9)
n.append(m)
m=[]
m.append(7)
m.append(8)
m.append(9)
n.append(m)

print(n)
# print(m[1,:])

datamatrix = np.array(n)
datamatrix = datamatrix.astype(np.float64)
print(datamatrix)

b,a = signal.butter(3,0.133,'low')
sf = signal.filtfilt(b,a,datamatrix[:,1])
print(sf)
# datamatrix[:1] = sf
for i in range (0,13):
    n[i][1] = sf[i]

print(n)
print(len(sf))