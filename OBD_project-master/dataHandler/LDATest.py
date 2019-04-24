from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words li+st
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# create sample documents
# doc_a = "In gensim a corpus is simply an object which, when iterated over, " \
#         "returns its documents represented as sparse vectors. " \
#         "In this case we are using a list of list of tuples. If you are not familiar with the vector space model, " \
#         "we’ll bridge the gap between raw strings, corpora and sparse vectors in the next tutorial on Corpora and Vector Spaces."
# doc_b = "Having bought numerous floor mats over the past 54 years, " \
#         "I can say without a doubt, these mats rank right up there with mats costing four to five times their cost. " \
#         "I couldn't be more impressed with the fit and finish. " \
#         "I would purchase these again without a second thought. Excellent product and unbelievably priced."
# doc_c = "So now suppose you have a set of documents. You’ve chosen some fixed number of K topics to discover, " \
#         "and want to use LDA to learn the topic representation of each document and the words associated to each topic. " \
#         "How do you do this? One way (known as collapsed Gibbs sampling) is the following:"
# doc_d = "At the beginning of the film, Liu Peiqiang, a Chinese astronaut, promises to his son Liu Qi of his eventual return before " \
#         "his mission to a space station that will help Earth navigate as it moves out of the Solar system, " \
#         "and hands guardianship of his son over to his father-in-law Han Zi'ang."
# doc_e = "Suppose you’ve just moved to a new city. You’re a hipster and an anime fan, so you want to know where the other hipsters and anime geeks tend to hang out. " \
#         "Of course, as a hipster, you know you can’t just ask, " \
#         "so what do you do?"

doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
doc_e = "Health professionals say that brocolli is good for your health."
#
# doc_a = "1 2 1 3 1 4 1 1 0 0 0 0 0 5 1 2 0 0" \
#         "0 1 2 0 0 0 0 0 0 1 0 0 2 3 1 0 0 0 7 6 1" \
#         "0 0 0 1 0 5 0 6 0 5 0 0 1 2 3 4 0 1 3 1 1 " \
#         "0 0 0 1 1 1 2 1 2 3 0 0 0 0 5 4 3 0 0 5 6 6 6 6 6 " \
#         "0 0 0 0 1 1 1 2 3 3 3 4 5 6 7 7 1 2 3 4 "

# doc_a = "1213 1411 0000 0512 " \
#         "0100 0000 1002 3100 0761" \
#         "0001 0506 0500 1234 0131  " \
#         "0001 1121 2300 0054 3005 6666  " \
#         "0000 1112 3334 5677 1234 "
# doc_a = '04000 42044 24024 02022 02000 24022 02206 02200 00624 04442 42004 44024 13412 22132 02460 62006 13130 20220 ' \
#        '22020 20131 32122 04204 20220 44422 20417 34402 04222 00002 00002 00200 20255 30420 '


# compile sample documents into a list
doc_set = [doc_a,doc_b,doc_c,doc_d]

# list for tokenized documents in loop
texts = []
print(doc_set)
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
ldamodel = Lda(corpus, num_topics=4,id2word = dictionary, passes=20)

# print most related words of each topic
print(ldamodel.print_topics(num_topics=4, num_words=3))

# print(ldamodel.print_topics(num_topics=2, num_words=20))

# fake a new document with numbers
vec = [(0, 2), (4, 1.6),(5,2),(1,1)]
# get the topic of new document
print(ldamodel[vec])