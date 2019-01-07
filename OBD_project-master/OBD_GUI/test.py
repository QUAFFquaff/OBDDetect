from numpy import *

matrix = array([(-0.146736425, -0.046935409, 0.98806148),
                (0.986075641, -0.085959069, 0.142358237),
                (0.078251203, 0.995192497, 0.05889519)])
print(matrix)

savetxt('orientation.txt', matrix)

myMatrix = loadtxt('orientation.txt')
print(myMatrix)