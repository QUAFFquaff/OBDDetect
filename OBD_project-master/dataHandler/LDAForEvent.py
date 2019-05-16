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
from fuzzywuzzy import fuzz
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
from gensim.test.utils import datapath


class LDAForEvent:
    height_weight = 8  # the weight of height in Manhattan distance
    delete_weight = 10  # the weight of delete a character when matching
    add_weight = 10  # the weight of add a character when matching
    ldamodel = LdaModel
    dictionary = corpora.Dictionary
    temp_dic = []
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
        values = ''
        start_time = float(table.row_values(0)[0])
        end_time = start_time + time_window
        x = start
        for x in range(end):
            # for x in range(start, end):
            row = table.row_values(x)

            flag += 1
            temp_s_time = float(row[0])
            temp_e_time = float(row[1])
            temp_char = row[2]
            # handle time
            if temp_e_time < end_time:  # the event is in the current time window
                values += temp_char
            elif temp_s_time > end_time:  # the event is out of the window
                start_time = end_time + 1
                end_time = start_time + time_window
                list_values += values + ' '
                values = temp_char
            elif temp_s_time < end_time < temp_e_time:
                start_time = temp_e_time + 1
                end_time = start_time + time_window
                list_values += values + temp_char+' '
                values = ''

        print([list_values])
        # datamatrix = np.array(list_values)
        # print(datamatrix)
        return list_values

    # # used to calculate the distance between two character
    # def calcDis(self, num_1, num_2):
    #     partA = self.height_weight * abs(num_1 / 4 - num_2 / 4)
    #     partB = abs(num_1 % 4 - num_2 % 4)
    #     return partA + partB

    # used to calculate the distance between two character
    # second vision
    # using characters a-z A-Z
    def calcDis(self, char_1, char_2):
        height1 = width1 = 0
        height2 = width2 = 0
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
        sum_distance = 0
        length_1 = len(s1)
        lenght_2 = len(s2)
        match_matrix = [[0 for i in range(len(s2))] for i in
                        range(len(s1))]  # length of s1 is numbers of rows; s2 are columns
        for i in range(len(s1)):
            for j in range(len(s2)):
                match_matrix[i][j] = self.calcDis(self, s1[i], s2[j])
        for i in range(len(s1)):
            match_matrix[i][0] = self.add_weight * i + match_matrix[0][0]
        for j in range(len(s2)):
            match_matrix[0][j] = self.delete_weight * j + match_matrix[0][0]
        for i in range(1, len(s1)):
            for j in range(1, len(s2)):
                match_matrix[i][j] = min(
                    match_matrix[i - 1][j - 1] + self.calcDis(self, s1[i],s2[j]),
                    match_matrix[i - 1][j] + self.add_weight, match_matrix[i][j - 1] + self.delete_weight)

        sum_distance = match_matrix[len(s1) - 1][len(s2) - 1]
        # print(sum_distance)
        max_unit = 65  # should change while the add_weight and delete_weight changed
        return (max_unit - sum_distance) / max_unit

    # doc is test document
    # dic is the dictionary of lda model
    def testEvent(self, doc,dic):
        testV = []
        # dic = self.dictionary
        for i in range(len(dic)):
            temp = [i, 0]
            testV.append(temp)
        for word in doc:
            f_max = 0
            flag = 1
            for index in range(len(dic)):
                grade = self.fuzzyEvent(self,word, dic[index])
                if f_max < grade:
                    f_max = grade
                    flag = 1
                elif f_max == grade:
                    flag += 1
            for index in range(len(dic)):
                grade = self.fuzzyEvent(self,word, dic[index])
                if f_max == grade:
                    testV[index][1] += 1 / flag
        # print(testV)
        # print(self.ldamodel[testV])
        return self.ldamodel[testV]

    def LDAtraining(self, doc_set):
        texts = []
        tokenizer = RegexpTokenizer(r'\w+')

        # create English stop words li+st
        en_stop = get_stop_words('en')

        # Create p_stemmer of class PorterStemmer
        p_stemmer = PorterStemmer()

        # loop through document list
        for i in doc_set:
            # clean and tokenize document string
            raw = i.lower()
            tokens = tokenizer.tokenize(raw)

            # remove stop words from tokens
            stopped_tokens = [i for i in tokens if not i in en_stop]

            # stem tokens
            stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

            # add tokens to list
            texts.append(stemmed_tokens)

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
        self.ldamodel = Lda(corpus, num_topics=4, random_state=9, id2word=dictionary)

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
        datamatrix1 = self.read_excel('ForLDA1alph.xls')
        datamatrix2 = self.read_excel('ForLDA2alph.xls')
        datamatrix3 = self.read_excel('ForLDA3alph.xls')
        datamatrix4 = self.read_excel('ForLDA4alph.xls')
        # print(datamatrix)
        # datamatrix = read_excel('ForLDA.xls')
        # print(datamatrix[0][102:180])
        # doc_set = [datamatrix[0], datamatrix[0][0:5] + datamatrix[0][8:17], datamatrix[0][18:31], datamatrix[0][85:105],
        #            datamatrix[0][127:150], "a8 8b1 ba1228b9"]
        doc_set = [
            datamatrix1,datamatrix2,datamatrix3,
                   datamatrix4]

        # print(doc_set)
        # doc_set = [datamatrix[0]]
        ldamodel2, dictionary = self.LDAtraining(self,doc_set)
        # ldamodel = LdaModel.load(datapath('model'))

    def LDALoad(self):
        self.ldamodel = LdaModel.load("fixed_time_window_lda.model")
        self.dictionary = Dictionary.load("lda_dictionary.model")
        print(self.dictionary)
        # print(len(self.dictionary))

    def LDATest(self, test):
        dictionary = Dictionary.load("lda_dictionary.model")
        result = self.testEvent(self, test,dictionary)
        return result


def main():
    ldamodel = LDAForEvent
    ldamodel.LDAPreProcessing(ldamodel)
    test = ['ah',"a","h"]
    result = ldamodel.LDATest(ldamodel,test)
    score =0
    for node in result:
        score+=(4-node[0])*25*node[1]
        print(node[1])
    print(score)
    # test = ['04000', '42044', '24024', '02022', '02000', '24022', '02206', '02200', '00624', '00624', '04442', '42004',
    #         '44024']
    # test = ['21222','01212','12121', '21012', '01010', '12121', '02120', '12010', '13312',
    #         '11011', '01010', '21212', '22222', '10020', '10312', '12122', '21212']
    # test = ['2122','01', '1212', '2121', '1', '01', '1', '1', '1','2120','20',  '31']
    # testEvent(test, ldamodel, dictionary)


if __name__ == '__main__':
    main()
