#!/usr/bin/env python

# encoding: utf-8

'''

@author: Quaff

@contact: Quaff.lyu@gmail.com

@file: LDAmodel.py

@time: 2019/3/8 10:11

@desc:

'''

import numpy as np
import guidedlda
import xlrd
import xlwt
from xlutils.copy import copy


def read_txt():
    with open('../data/ABCD0000.txt', 'r') as f:
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

text1 = read_txt()


# Guided LDA with seed topics.
# old seeds
# seed_topic_list = [['a', 'h', 'o', 'v','vo', 'hho','hhah','avoa','haa','vvvv', 'ova', 'avavv', 'ahao', 'aoah',],
#                    ['io', 'b', 'i',  'bi','va','vv','wwhhi','bbbi','abovb','ovppah','avhvowa','ai','ih','wa','ba'],
#                    ['iwwp', 'pb', 'pb', 'wbi', 'bi', 'p', 'pi', 'pwp' ,'xi','ixipp','bwbw', 'iwx','ibpxiix','iq','pq','px','ix','ipi','pwi'],
#                    ['xcqxx', 'cq',  'wx', 'cii','jcc', 'qq', 'jcxqc','cq', 'wj','j','q' 'jx', 'x', 'c', 'cjc']
#                    ]
seed_topic_list = [['a', 'b', 'd', 'c', 'cd', 'bbd', 'bbab', 'acda', 'baa', 'cccc', 'dca', 'acacc', 'abad', 'adab'],
                   ['nd', 'm', 'n', 'mn', 'ca', 'cc', 'ppbbn', 'mmmn', 'amdcm', 'dcooab', 'acbcdpa', 'an', 'nb', 'pa', 'ma'],
                   ['nppo', 'om', 'om', 'pmn', 'mn', 'on', 'opo', 'zn', 'nznoo', 'mpmp', 'npz', 'nmoznnz'],
                   ['x','y', 'z', 'w','zwyzz', 'wy', 'pz', 'wnn', 'xww', 'yy', 'xwzyw', 'wy', 'px',  'yxz', 'wxw']]

# seed_topic_list = [['aaa'],
#                    ['ccc']
#                    ]
# X = guidedlda.datasets.load_data(guidedlda.datasets.NYT)
# vocab = guidedlda.datasets.load_vocab(guidedlda.datasets.NYT)
# word2id = dict((v, idx) for idx, v in enumerate(vocab))
n_top_words = 5344
TOPICS = 4


def write_excel_xls(path, sheet_name, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    for name in sheet_name:
        sheet = workbook.add_sheet(name)  # 在工作簿中新建一个表格
        for i in range(0, index):
            for j in range(0, len(value[i])):
                sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿
    print("xls格式表格写入数据成功！")


def write_excel_xls_append(path,sheet, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheet)  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i + rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")

book_name_xls = 'xls result saving.xls'

sheet_name_xls = ['without  or', 'without  op', 'with  or', 'with  op']

value_title = [["test case", "score", "group0", "group1", "group2", "group3"], ]

def guidedldatest(X, vocab, word2id):
    print(X.shape)
    # Normal LDA without seeding
    model = guidedlda.GuidedLDA(n_topics=TOPICS, n_iter=1000, random_state=9, refresh=20)
    model.fit(X)
    sortedresult = [[], [], [], []]
    topic_word = model.topic_word_
    # n_top_words = 2
    # print(topic_word.shape)
    for i, topic_dist in enumerate(topic_word):

        # print(topic_dist.shape)
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words + 1):-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
        sortedresult[i].append(topic_words)


    # test lda model
    tests = ['a', 'b', 'abbca', 'ccbba', 'dabdda',
             'm', 'ammp', 'non', 'mmdn', 'oaa',
             'o', 'wwp', 'xp', 'xnp', 'ppopn',
             'w', 'xzzmz', 'ywzzyz', 'wywyzyy', 'zww']

    max_len = 5344
    result = []
    for test in tests:
        temp = [int(np.argwhere(i[0] == test)) for i in sortedresult]
        # normal one
        output_o = [(max_len - index) / (4 * max_len - sum(temp)) for index in temp]
        line = [test,str(get_score(output_o)),str(output_o[0]),str(output_o[1]),str(output_o[2]),str(output_o[3])]
        result.append(line)
    write_excel_xls(book_name_xls, sheet_name_xls, value_title)
    write_excel_xls_append(book_name_xls, sheet_name_xls[0], result)
    print('write success')
    print('-----------------------------------------------------')

    for test in tests:
        temp = [int(np.argwhere(i[0] == test)) for i in sortedresult]
        # normal one

        # half len optimize
        half_len = 5344 / 2
        for i in range(len(temp)):
            if temp[i] > half_len:
                temp[i] = half_len
        output = [(half_len - index) / (4 * half_len - sum(temp)) for index in temp]
        # output = [ (max_len - index)/(4*max_len - sum(temp)) for index in temp]
        line = [test,str(get_score(output)),str(output[0]),str(output[1]),str(output[2]),str(output[3])]
        result.append(line)
    write_excel_xls_append(book_name_xls,sheet_name_xls[1],  result)
    print('write success ',book_name_xls[1])
    print('-----------------------------------------------------')



    # model with seeds


    model = guidedlda.GuidedLDA(n_topics=TOPICS, n_iter=1000, random_state=9, refresh=20)



    seed_topics = {}
    for t_id, st in enumerate(seed_topic_list):
        for word in st:
            seed_topics[word2id[word]] = t_id

    model.fit(X, seed_topics=seed_topics, seed_confidence=0.15)

    topic_word = model.topic_word_
    sortedresult = [[],[],[],[]]
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words + 1):-1]
        sortedresult[i].append(topic_words)

        print('Topic {}: {}'.format(i, ' '.join(topic_words)))

    print(sortedresult)
    max_len = 5344
    for test in tests:
        temp = [int(np.argwhere(i[0]==test)) for i in sortedresult]

        # normal one
        output_o = [(max_len - index) / (4 * max_len - sum(temp)) for index in temp]

        line = [test, str(get_score(output_o)), str(output_o[0]), str(output_o[1]), str(output_o[2]), str(output_o[3])]
        result.append(line)
    write_excel_xls_append(book_name_xls, sheet_name_xls[2],  result)
    print('write success')
    print('-----------------------------------------------------')

    for test in tests:
        temp = [int(np.argwhere(i[0] == test)) for i in sortedresult]

        # half len optimize
        half_len = 5344/2
        for i in range(len(temp)):
            if temp[i] > half_len:
                temp[i] = half_len
        output = [ (half_len - index)/(4*half_len - sum(temp)) for index in temp]
        # output = [ (max_len - index)/(4*max_len - sum(temp)) for index in temp]
        line = [test,str(get_score(output)),str(output[0]),str(output[1]),str(output[2]),str(output[3])]
        result.append(line)
    write_excel_xls_append(book_name_xls, sheet_name_xls[3], result)
    print('write success ',book_name_xls[1])
    print('-----------------------------------------------------')



def get_score(output):
    score = 0

    for item in range(len(output)):
        score += (4-item)*25*output[item]
    return score



def transTextIntoMatrix(text):
    """

    :type text: input text
    """
    vocab = tuple(set(np.hstack(text).tolist()))
    print(vocab)

    word2id = dict((v, idx) for idx, v in enumerate(vocab))

    print(word2id)
    matrix = np.zeros((len(text), len(vocab)), dtype=np.int64)

    for rows in range(len(matrix)):
        for item in range(len(text[rows])):
            # print(item)
            # print(word2id[text[rows][item]])
            matrix[rows][word2id[text[rows][item]]] += 1

    return matrix, vocab, word2id


matrix, vocab, word2id = transTextIntoMatrix(text1)
guidedldatest(matrix, vocab, word2id)
