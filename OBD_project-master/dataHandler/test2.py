#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 12/3/2019 0:24
# @Author  : Haoyu Lyu
# @File    : test2.py
# @Software: PyCharm



import numpy as np
import guidedlda


X = guidedlda.datasets.load_data(guidedlda.datasets.NYT)


vocab = guidedlda.datasets.load_vocab(guidedlda.datasets.NYT)
print(len(vocab))
word2id = dict((v, idx) for idx, v in enumerate(vocab))

print(word2id)
# Normal LDA without seeding
# model = guidedlda.GuidedLDA(n_topics=5, n_iter=100, random_state=9, refresh=20)
# model.fit(X)
#
# topic_word = model.topic_word_
# print(topic_word)