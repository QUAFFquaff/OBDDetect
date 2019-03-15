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
from fuzzywuzzy import fuzz
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from xlwt import *
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
from gensim.test.utils import get_tmpfile
import gensim
from gensim.test.utils import datapath


def read_excel(file):
    data = xlrd.open_workbook(file)
    table = data.sheets()[0]

    start = 0  # 开始的行
    end = 164  # 结束的行
    rows = end - start
    list_values = ""
    flag = 0
    values = ''
    for x in range(start, end):
        row = table.row_values(x)
        # orientation X,Y; acceleration X,Y, SMA X,Y; time
        for i in [2]:
            # print(value)
            flag += 1
            values += str(row[i][0])
        if flag == 5:
            flag = 0
            list_values+=values+' '
            values = ''
    print([list_values])
    # datamatrix = np.array(list_values)
    # print(datamatrix)
    return [list_values]

def fuzzyEvent(s1,s2):
    return (fuzz.ratio(s1, s2))


def testEvent(doc,ldamodel,dic):
    testV = []
    for i in range(len(dic)):
        temp = [ i , 0]
        testV.append(temp)
    for word in doc:
        f_max = 0
        flag = 1
        for index in range(len(dic)):
            grade = fuzzyEvent(word, dic[index])
            if f_max < grade:
                f_max = grade
                flag = 1
            elif f_max == grade:
                flag += 1
        for index in range(len(dic)):
            grade = fuzzyEvent(word, dic[index])
            if f_max == grade:
                testV[index][1] += 1/flag
    # print(testV)
    print(ldamodel[testV])

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
    ldamodel = Lda(corpus, num_topics=4, eval_every=10,id2word=dictionary, passes=20,iterations=5000)

    # print most related words of each topic
    print(ldamodel.print_topics(num_topics=4, num_words=9))

    # print(ldamodel.print_topics(num_topics=2, num_words=20))

    # get the topic of new document
    lda_file = datapath('model')
    ldamodel.save(lda_file)
    dic_file = datapath("dictionary")
    dictionary.save(dic_file)

    return ldamodel, dictionary

def main():


    # testEvent('its has been a long time since we last meet')
    datamatrix = read_excel('ForLDA.xls')
    # # print(datamatrix)
    ldamodel,dictionary = LDAtraining(datamatrix,[])
    ldamodel = LdaModel.load(datapath('model'))
    dictionary = Dictionary.load(datapath('dictionary'))
    print(len(dictionary))
    test = ['04000', '42044', '24024', '02022', '02000', '24022', '02206', '02200', '00624', '00624', '04442', '42004', '44024']
    testEvent(test,ldamodel,dictionary)

if __name__ == '__main__':
    main()