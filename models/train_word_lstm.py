'''Example script to generate text from Nietzsche's writings.

At least 20 epochs are required before the generated text
starts sounding coherent.

It is recommended to run this script on GPU, as recurrent
networks are quite computationally intensive.

If you try this script on new data, make sure your corpus
has at least ~100k characters. ~1M is better.
'''

from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys

#path = get_file('nietzsche.txt', origin="https://s3.amazonaws.com/text-datasets/nietzsche.txt")
#path = get_file('combined_queryparser.txt',origin="/if24/mr5ba/Masud/deeplearning/dataset/combined_queryparser.txt")
#path = "/if24/mr5ba/Masud/deeplearning/dataset/combined_queries.txt"
path = "/if24/mr5ba/Masud/PythonProjects/dataset/autocode_data/train_data_text.txt"

text = open(path).read().lower()
text_words = text.split(" ")
print("Len words = "+str(len(text_words)))
#print (text_words)

#print('corpus length:', len(text))
#print('Text length = ', len(text.split()))
chars = sorted(list(set(text)))
vocab = sorted(list(set(text_words)))
print("Len vocablary = "+str(len(vocab)))
np.save("vocabulary.txt", vocab)
#exit()
#print ('Total chars = ',chars)
#print (list(set(text)))
#print('total chars:', len(chars))
word_indices = dict((c, i) for i, c in enumerate(vocab))
indices_word = dict((i, c) for i, c in enumerate(vocab))
print (word_indices['for'])
print (indices_word[20])


# cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
step = 3
sentences = []
next_words = []
for i in range(0, len(text_words) - maxlen, step):
    sentences.append(text_words[i: i + maxlen])
    next_words.append(text_words[i + maxlen])
print ("sen = "+str(sentences[0]))
print ("next = "+str(next_words[0]))
print ("======================\n")
print ("sen = "+str(sentences[1]))
print ("next = "+str(next_words[1]))
print ("======================\n")
print ("sen = "+str(sentences[2]))
print ("next = "+str(next_words[2]))

print('nb sequences:', len(sentences))
#exit()

#print ("Sentences: \n", sentences)
print('Vectorization...')
X = np.zeros((len(sentences), maxlen, len(vocab)), dtype=np.bool)
y = np.zeros((len(sentences), len(vocab)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, word in enumerate(sentence):
        X[i, t, word_indices[word]] = 1
    y[i, word_indices[next_words[i]]] = 1

#print ("X ", X)
#print("y ", y)
# build the model: a single LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, len(vocab))))
model.add(Dense(len(vocab)))
model.add(Activation('softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)
# train the model, output generated text after each iteration
for iteration in range(1, 20):#changed
    print('Iteration', iteration)
    model.fit(X, y, batch_size=128, nb_epoch=1)
    print ("Saving model")
    model.save("code_word_lstm_20.h5",True)
    print("Model Saved")
