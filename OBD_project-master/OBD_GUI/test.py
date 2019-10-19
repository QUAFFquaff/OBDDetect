#!/usr/bin/env python

# encoding: utf-8

'''

@author: Quaff

@contact: Quaff.lyu@gmail.com

@file: LDAmodel.py

@time: 2019/3/8 10:11

@desc:

'''

import xlrd
import numpy as np
#from fuzzywuzzy import fuzz
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
from gensim.test.utils import datapath
import time

class LDAForEvent:
    height_weight = 8  # the weight of height in Manhattan distance
    delete_weight = 10  # the weight of delete a character when matching
    add_weight = 10  # the weight of add a character when matching
    ldamodel = LdaModel
    dictionary = corpora.Dictionary
    temp_dic = []
    dictionary = Dictionary.load("lda_dictionary.model")
    # load raw data into workspace
    @staticmethod
    def read_excel(file):
        time_window = 40 * 1000
        data = xlrd.open_workbook(file)
        table = data.sheets()[0]

        start = 0  # 开始的行
        # end = 164  # 结束的行
        end = len(table.col_values(0))  # from the first line to last line
        rows = end - start
        list_values = ""
        flag = 0
        word_brffer = ''
        start_time = float(table.row_values(0)[0])
        end_time = start_time + time_window
        x = start
        while x <end:
            # for x in range(start, end):
            row = table.row_values(x)

            flag += 1
            temp_s_time = float(row[0])
            temp_e_time = float(row[1])
            temp_char = row[2]
            # handle time
            if temp_e_time < end_time:  # the event is in the current time window
                word_brffer += temp_char
            elif temp_s_time > end_time:  # the event is out of the window
                start_time = end_time
                end_time = start_time + time_window
                list_values += word_brffer + ' '
                word_brffer = ""
                x-=1
            elif temp_s_time < end_time < temp_e_time:
                start_time = temp_e_time + 1
                end_time = start_time + time_window
                list_values += word_brffer + temp_char+' '
                word_brffer = ''
            x+=1

        # print([list_values])
        # datamatrix = np.array(list_values)
        # print(datamatrix)
        return list_values


    # used to calculate the distance between two character
    # second vision
    # using characters a-z A-Z
    def calcDis(self, char_1, char_2):

        if ord(char_1)>140:
            height1 = (ord(char_1) - ord('a'))%7
            width1 = (ord(char_1) - ord('a') )/7
        else:
            height1 = (ord(char_1) - ord('C'))%7
            width1 = (ord(char_1) - ord('C') )/7
        if ord(char_2)>140:
            height2 = (ord(char_2) - ord('a'))%7
            width2 = (ord(char_2) - ord('a') )/7
        else:
            height2 = (ord(char_2) - ord('C'))%7
            width2 = (ord(char_2) - ord('C') )/7
        partA = self.height_weight * abs(height1 - height2)
        partB = abs(width1 - width2)
        return partA + partB

    #   fuzzyEvent2
    #   used to match words with different length
    def fuzzyEvent(self, s1, s2):
        match_matrix = [[0 for i in range(len(s2)+1)] for i in
                        range(len(s1)+1)]  # length of s1 is numbers of rows; s2 are columns

        for i in range(len(s1)):
            match_matrix[i][0] = self.add_weight * i
        for j in range(len(s2)):
            match_matrix[0][j] = self.delete_weight * j
        for i in range(1, len(s1)+1):
            for j in range(1, len(s2)+1):
                match_matrix[i][j] = min(
                    match_matrix[i - 1][j - 1] + self.calcDis(self, s1[i-1],s2[j-1]),
                    match_matrix[i - 1][j] + self.add_weight, match_matrix[i][j - 1] + self.delete_weight)

        sum_distance = match_matrix[len(s1)][len(s2)]
        max_unit = 100  # should change while the add_weight and delete_weight changed
        return (max_unit - sum_distance) / max_unit

    # doc is test document
    # dic is the dictionary of lda model
    def testEvent(self, doc,dic=[]):
        if len(dic)==0:
            dic = self.dictionary
        testV = []
        for i in range(len(dic)):
            temp = [i, 0]
            testV.append(temp)
        for word in doc:
            f_max = 0
            flag = 1

            temp_testV = [0 for i in range(len(testV))]
            for index in range(len(dic)):
                if dic[index] == word:
                    testV[index][1] += 1
                    break
                if abs(len(word)-len(dic[index]))>3:
                    continue
                grade = self.fuzzyEvent(self,word, dic[index])
                if f_max < grade:
                    f_max = grade
                    flag = 1
                elif f_max == grade:
                    flag += 1
                temp_testV[index] = grade
            for index in range(len(testV)):
                if f_max == temp_testV[index]:
                    testV[index][1] += 1 / flag
        return self.ldamodel[testV]

    def LDALoad(self):
        self.ldamodel = LdaModel.load("fixed_time_window_lda.model")
        self.dictionary = Dictionary.load("lda_dictionary.model")
        print(self.dictionary)
        # print(len(self.dictionary))

    def LDATest(self, test):
        result = self.testEvent(self, test,self.dictionary)
        return result

def read_txt():
    with open('fakeData.txt', 'r') as f:
        lines = f.readlines()
    file_list = []
    for line in lines:
        pattern_list = []
        patterns = line.split("\'")
        for i in range(len(patterns)):
            if i % 2 != 0:
                pattern_list.append(patterns[i])
        file_list.append(pattern_list)
    return file_list



def main():
    file_list = read_txt()
    ldamodel = LDAForEvent
    # ldamodel.LDAPreProcessing(ldamodel)
    ldamodel.LDALoad(ldamodel)
    file_score = []
    factor = np.array([75,100,50,25])
    total_score = []
    for file in file_list:
        scores = []

        for pattern in file:
            result = ldamodel.testEvent(ldamodel, pattern)
            nums = []
            score = 0
            for node in result:
                if 0 == node[0]:
                    score += 75 * node[1]
                elif 1 == node[0]:
                    score += 100 * node[1]
                elif 2 == node[0]:
                    score += 50 * node[1]
                elif 3 == node[0]:
                    score += 25 * node[1]

            scores.append(score)
        file_score.append(scores)

    print('down')
    f = open('scores00.txt', 'a')
    # for data in file_score:
    #
    f.write(str(file_score))
    f.close()

if __name__ == '__main__':
    main()