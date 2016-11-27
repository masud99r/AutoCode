
from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
from keras.models import load_model
import numpy as np
import random
import sys
import re

vocab = np.load("vocabulary.txt.npy")
print("Len vocablary = "+str(len(vocab)))

word_indices = dict((c, i) for i, c in enumerate(vocab))
indices_word = dict((i, c) for i, c in enumerate(vocab))

path_test = "/if24/mr5ba/Masud/PythonProjects/dataset/autocode_data/test_data_code.txt"
test_text_lower = open(path_test).read().lower()
test_text = test_text_lower.split(" ")
word_indices = dict((c, i) for i, c in enumerate(vocab))
indices_word = dict((i, c) for i, c in enumerate(vocab))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
step = 3
sentences = []
next_chars = []

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

model = load_model("bidirectional_lstm_20.h5")
#model = load_model("rnn_code_20.h5")

start_index =-1
seglen = 10

Hx = 0
for i in range(50):
    start_index += 1
    if start_index + seglen < len(test_text)-1: #reserve last char to get probability
        sentence = test_text[start_index: start_index + seglen]
    else:
        break
    word_to_test = test_text[start_index+seglen]
    if word_to_test not in vocab:
        print (word_to_test +" not in vocabulary")
        continue
    x = np.zeros((1, maxlen, len(vocab)))

    for t, word in enumerate(sentence):
        if word not in vocab:
            continue
        x[0, t, word_indices[word]] = 1

    preds = model.predict(x, verbose=0)[0]
    index_c = word_indices[word_to_test]
    list_pred = preds.tolist()
    prob_c = list_pred[index_c]
    Hx = Hx + prob_c * np.log2(prob_c)

Hx = Hx * (-1)
perplexity = np.power(2,Hx)
print ("Entropy = "+str(Hx))
print ("Perplexity = "+str(perplexity))