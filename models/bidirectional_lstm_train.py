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
from keras.layers import Dense, Activation, Dropout, Bidirectional, Embedding
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys


path = "/if24/mr5ba/Masud/PythonProjects/dataset/autocode_data/train_data_code.txt"

text = open(path).read().lower()
text_words = text.split(" ")
print("Total tokens = "+str(len(text_words)))

vocab = sorted(list(set(text_words)))
print("Len vocablary = "+str(len(vocab)))
np.save("vocabulary.txt", vocab)

word_indices = dict((c, i) for i, c in enumerate(vocab))
indices_word = dict((i, c) for i, c in enumerate(vocab))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
step = 3
sentences = []
next_words = []
for i in range(0, len(text_words) - maxlen, step):
    sentences.append(text_words[i: i + maxlen])
    next_words.append(text_words[i + maxlen])

print('nb sequences:', len(sentences))

print('Vectorization...')
X = np.zeros((len(sentences), maxlen, len(vocab)), dtype=np.bool)
y = np.zeros((len(sentences), len(vocab)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, word in enumerate(sentence):
        X[i, t, word_indices[word]] = 1
    y[i, word_indices[next_words[i]]] = 1
max_features = 3
# build the model: a single LSTM
print('Build model...')
model = Sequential()
#model.add(Embedding(max_features, 128, input_length=maxlen))#first layer must be input
model.add(Bidirectional(LSTM(128),input_shape=(maxlen, len(vocab))))
model.add(Dense(len(vocab)))
model.add(Activation('softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)
# train the model, output generated text after each iteration
for iteration in range(1, 20):#changed
    print('Iteration', iteration)
    model.fit(X, y, batch_size=128, nb_epoch=1)

print ("Saving model")
print("Model Saved: bidirectional_lstm_20.h5")
model.save("bidirectional_lstm_20.h5",True)
