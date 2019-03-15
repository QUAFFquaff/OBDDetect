#!/usr/bin/env python

# encoding: utf-8

'''

@author: Quaff

@contact: Quaff.lyu@gmail.com

@file: LDAmodel.py

@time: 2019/3/8 10:11

@desc:

'''

# load raw data into workspace
import xlrd
import numpy as np
from xlwt import *
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim


def read_excel(file):
    data = xlrd.open_workbook(file)
    table = data.sheets()[0]
    # print(table)
    # nrows = table.nrows #行数
    # ncols = table.ncols #列数
    # c1=arange(0,nrows,1)
    # print(c1)

    start = 0  # 开始的行
    end = 4902  # 结束的行
    rows = end - start
    list_values = []
    for x in range(start, end):
        values = []
        row = table.row_values(x)
        # orientation X,Y; acceleration X,Y, SMA X,Y; time
        for i in [9]:
            # print(value)
            values.append(row[i])
            list_values.append(str(row[i]))
    # print(list_values)
    datamatrix = np.array(list_values)
    # print(datamatrix)
    return list_values


def checkMotion(dataMatrix, windowSize):
    flag = []
    startPoint = endPoint = 0
    counter = 0
    while startPoint < len(dataMatrix):
        accF = braF = turnF = 0
        endPoint = startPoint
        # find all data in the same data set






        while endPoint > 0 and (int(dataMatrix[startPoint][0]) - int(dataMatrix[endPoint][0])) <= windowSize:
            d = int(dataMatrix[startPoint][0]) - int(dataMatrix[endPoint][0])
            print(dataMatrix[startPoint][0])
            print(".--.", int(dataMatrix[endPoint][0]))
            print(".--.", int(dataMatrix[endPoint][0]))
            print(int(dataMatrix[startPoint][0]) - int(dataMatrix[endPoint][0]))
            if dataMatrix[endPoint][2] == 'speedup':
                accF += 1
            elif dataMatrix[endPoint][2] == 'swerve':
                turnF += 1
            elif dataMatrix[endPoint][2] == 'brake':
                braF += 1
            endPoint -= 1
        flag.append([accF, turnF, braF])
        startPoint += 1
    print(flag)
    print(len(flag))
    print(len(flag[0]))
    return flag


def LDAtraining(doc_set, test_set):
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
    ldamodel = Lda(corpus, num_topics=4,alpha='auto', id2word=dictionary, passes=20)

    # print most related words of each topic
    print(ldamodel.print_topics(num_topics=4, num_words=5))

    # print(ldamodel.print_topics(num_topics=2, num_words=20))

    # fake a new document with numbers
    vec = [(0, 2), (4, 1.6), (5, 2), (1, 1)]
    # get the topic of new document
    print(ldamodel[vec])
    pass

def main():
    datamatrix = read_excel('label_data3.8.xlsx')
    print(datamatrix)
    LDAtraining(datamatrix,[])

if __name__ == '__main__':
    main()