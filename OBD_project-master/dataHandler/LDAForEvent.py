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

    def read_txt(self):
        # with open('../data/ABCDFakeDataForEvent.txt', 'r') as f:
        # with open('../data/newfakeData0.txt', 'r') as f:
        with open('../data/fakeDataForEvent.txt', 'r') as f:
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

    def LDAtraining(self, doc_set=[]):
        texts = []
        tokenizer = RegexpTokenizer(r'\w+')

        # create English stop words li+st
        # en_stop = get_stop_words('en')

        # Create p_stemmer of class PorterStemmer
        p_stemmer = PorterStemmer()

        # loop through document list
        temp_context = []
        for i in doc_set:
            for j in i.split(" "):
                if j != "":
                    temp_context.append(j)

            # add tokens to list
            texts.append(temp_context)
            temp_context = []
        texts = self.read_txt(self)
        print(texts)

        # turn our tokenized documents into a id <-> term dictionary
        dictionary = corpora.Dictionary(texts)

        # convert tokenized documents into a document-term matrix
        corpus = [dictionary.doc2bow(text) for text in texts]

        Lda = gensim.models.ldamodel.LdaModel

        # generate LDA model
        #   passes (int, optional) – Number of passes through the corpus during training.
        #   iterations (int, optional) – Maximum number of iterations through the corpus
        #                                 when inferring the topic distribution of a corpus.
        #   eval_every (int, optional) – Log perplexity is estimated every that many updates.
        #                                 Setting this to one slows down training by ~2x.
        #   distributed (bool, optional) – Whether distributed computing should be used to accelerate training.
        #   update_every (int, optional) – Number of documents to be iterated through for each update.
        #                                    Set to 0 for batch learning,
        #                                    > 1 for online iterative learning.
        # ldamodel = Lda(corpus, num_topics=4, eval_every=10, id2word=dictionary, passes=900, iterations=500)

        # best case of old one
        self.ldamodel = Lda(corpus, num_topics=4, random_state=0,iterations=600, id2word=dictionary)
        # self.ldamodel = Lda(corpus, num_topics=4, random_state=1,iterations=10000, id2word=dictionary)

        # print most related words of each topic
        print(self.ldamodel.print_topics(num_topics=4, num_words=6))

        # print(ldamodel.print_topics(num_topics=2, num_words=20))

        # get the topic of new document
        lda_file = datapath('model')
        self.ldamodel.save(lda_file)
        self.ldamodel.save("fixed_time_window_lda.model")
        dic_file = datapath("dictionary")
        dictionary.save(dic_file)
        dictionary.save("lda_dictionary.model")

        return self.ldamodel, dictionary

    def LDAPreProcessing(self):

        doc_set = []

        ldamodel2, dictionary = self.LDAtraining(self,doc_set)
        # ldamodel = LdaModel.load(datapath('model'))

    def LDALoad(self):
        self.ldamodel = LdaModel.load("fixed_time_window_lda.model")
        self.dictionary = Dictionary.load("lda_dictionary.model")
        print(self.dictionary)
        # print(len(self.dictionary))

    def LDATest(self, test):
        result = self.testEvent(self, test,self.dictionary)
        return result


def main():
    ldamodel = LDAForEvent
    ldamodel.LDAtraining(ldamodel)
    ldamodel.LDAPreProcessing(ldamodel)
    ldamodel.LDALoad(ldamodel)


    tests = ['a', 'dcbadca', 'nodmmp', 'pn', 'zyz', 'w', 'xzzzx']
    tests = ['a', 'h', 'ahhva', 'vvhha', 'oahooa',
             'b', 'abbw', 'ipi', 'bboi', 'paa',
             'p', 'ccw', 'jw', 'jiw', 'wwpwi',
             'c', 'jxxbx', 'qcxxqx', 'cqcqxqq', 'xcc']
    for test in tests:
        result = ldamodel.LDATest(ldamodel, test)
        score = 0
        for node in result:
            if 0==node[0]:
                score+=75*node[1]
            elif 1 == node[0]:
                score += 100 * node[1]
            elif 2 == node[0]:
                score += 50 * node[1]
            elif 3 == node[0]:
                score += 25 * node[1]

        # print('test case:', test, 'score', score, 'result', result)
        # print(test)
        # print(score)
        print(result[3][1])


if __name__ == '__main__':
    main()
