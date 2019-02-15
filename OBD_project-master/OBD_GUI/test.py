from numpy import *

matrix = array([(-0.146736425, -0.046935409, 0.98806148),
                (0.986075641, -0.085959069, 0.142358237),
                (0.078251203, 0.995192497, 0.05889519)])
print(matrix)

matrix1 = array([(1,1,3),
                 (2,4,5),
                 (5,4,3)])
matrix2 = array([2,4,1])

print(dot(matrix1,matrix2))
print(matrix1)