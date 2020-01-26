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

def read_txt():
    with open('../data/fakeData.txt', 'r') as f:
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

text2 = [['aaa', 'aaa'],
         ['ccc', 'ccc'],
         ['bbb', 'ccc'],
         ['ddd', 'eee']]

# Guided LDA with seed topics.
seed_topic_list = [['a', 'h', 'o', 'v','vo', 'hho','hhah','avoa','haa','vvvv', 'ova', 'avavv', 'ahao', 'aoah',],
                   ['io', 'b', 'i',  'bi','va','vv','wwhhi','bbbi','abovb','ovppah','avhvowa','ai','ih','wa','ba'],
                   ['iwwp', 'pb', 'pb', 'wbi', 'bi', 'p', 'pi', 'pwp' ,'xi','ixipp','bwbw', 'iwx','ibpxiix','iq','pq','px','ix','ipi','pwi'],
                   ['xcqxx', 'cq',  'wx', 'cii','jcc', 'qq', 'jcxqc','cq', 'wj','j','q' 'jx', 'x', 'c', 'cjc']
                   ]
# seed_topic_list = [['aaa'],
#                    ['ccc']
#                    ]
# X = guidedlda.datasets.load_data(guidedlda.datasets.NYT)
# vocab = guidedlda.datasets.load_vocab(guidedlda.datasets.NYT)
# word2id = dict((v, idx) for idx, v in enumerate(vocab))
n_top_words = 5344
TOPICS = 4


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
    tests = ['h', 'a', 'qq', 'cx', 'hvh']
    max_len = 5344
    for test in tests:
        temp = [int(np.argwhere(i[0] == test)) for i in sortedresult]

        # half len optimize
        half_len = 5344 / 2
        for i in range(len(temp)):
            if temp[i] > half_len:
                temp[i] = half_len
        output = [(half_len - index) / (4 * half_len - sum(temp)) for index in temp]
        # output = [ (max_len - index)/(4*max_len - sum(temp)) for index in temp]
        print('test', test, ':', output)


    model = guidedlda.GuidedLDA(n_topics=TOPICS, n_iter=1000, random_state=9, refresh=20)

    seed_topics = {}
    for t_id, st in enumerate(seed_topic_list):
        for word in st:
            seed_topics[word2id[word]] = t_id

    model.fit(X, seed_topics=seed_topics, seed_confidence=0.15)

    topic_word = model.topic_word_
    # print('model topic words')
    # print(model.topic_word_)
    sortedresult = [[],[],[],[]]
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words + 1):-1]
        sortedresult[i].append(topic_words)

        print('Topic {}: {}'.format(i, ' '.join(topic_words)))

    print(sortedresult)
    tests = ['h','a','qq','cx','hvh']
    max_len = 5344
    for test in tests:
        temp = [int(np.argwhere(i[0]==test)) for i in sortedresult]

        # half len optimize
        half_len = 5344/2
        for i in range(len(temp)):
            if temp[i] > half_len:
                temp[i] = half_len
        output = [ (half_len - index)/(4*half_len - sum(temp)) for index in temp]
        # output = [ (max_len - index)/(4*max_len - sum(temp)) for index in temp]
        print('test',test,':',output)



def testText(text, result):
    output = []


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
