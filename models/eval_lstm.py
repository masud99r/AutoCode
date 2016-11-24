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
from keras.models import load_model
import numpy as np
import random
import sys
import re

#path = get_file('nietzsche.txt', origin="https://s3.amazonaws.com/text-datasets/nietzsche.txt")
#print (path)
path = "/if24/mr5ba/Masud/PythonProjects/dataset/autocode_data/train_data_code.txt"
#path = get_file('combined_queryparser.txt',origin="/if24/mr5ba/Masud/deeplearning/dataset/combined_queryparser.txt")
path_test = "/if24/mr5ba/Masud/PythonProjects/dataset/autocode_data/test_data_code.txt"
text = open(path).read().lower()
#text = re.sub('[^A-Za-z0-9 ]+', '', text_garbase)
test_text_lower = open(path_test).read().lower()
test_text = re.sub('[^A-Za-z0-9 ]+', '', test_text_lower)

#print('corpus length:', len(text))
#print('Text length = ', len(text.split()))
chars = sorted(list(set(text)))
#print ('Total chars = ',chars)
#print (list(set(text)))
#print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

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

generated = 'START '
#sentence ="asily wiped out, easily extinguished, by".lower()
char_seq=''
#print ("Sentence len = ", len(sentence))
model = load_model("code_char_lstm_20.h5")
'''
for i in range(400):
    x = np.zeros((1, maxlen, len(chars)))
    for t, char in enumerate(sentence):
        x[0, t, char_indices[char]] = 1.
        char_seq = char_seq+char

    preds = model.predict(x, verbose=0)[0]
    next_index = sample(preds,0.5)
    next_char = indices_char[next_index]

    generated += next_char
    sentence = sentence[1:] + next_char
    sys.stdout.write(next_char)
    sys.stdout.flush()
print()
print(generated)
'''

#start_index = random.randint(0, len(test_text) - maxlen - 1)


start_index =0
generated = ''
seglen = 10
#sentence = test_text[start_index: start_index + seglen]
#generated += sentence
#print('----- Generating with seed: "' + sentence + '"')
#sys.stdout.write(generated)

Hx = 0
print("Vocabulary length = "+str(len(chars)))
for i in range(50):
    if start_index + seglen < len(test_text)-1: #reserve last char to get probability
        sentence = test_text[start_index: start_index + seglen]
    char_to_test = test_text[start_index+seglen]

    x = np.zeros((1, maxlen, len(chars)))

    #for t, char in enumerate(chars):
    #    x[0, t, char_indices[char]] = 0

    for t, char in enumerate(sentence):
        if char not in sentence:
            continue
        x[0, t, char_indices[char]] = 1

    #print ("X= ",len(x.tolist()))
    #print("X= ", len(x.tolist()[0]))
    preds = model.predict(x, verbose=0)[0]
    index_c = char_indices[char_to_test]
    #print preds[1]
    list_pred = preds.tolist()
    #print ("Sentence: "+sentence)
    prob_c = list_pred[index_c]
    Hx = Hx + prob_c * np.log2(prob_c)

    #print(char_to_test+" = "+str(prob_c))
    start_index += 1
Hx = Hx * (-1)
perplexity = np.power(2,Hx)
print ("Entropy = "+str(Hx))
print ("Perplexity = "+str(perplexity))
'''
for diversity in [0.2, 0.5, 1.0, 1.2]:
    print()
    print('----- diversity:', diversity)
    start_index = random.randint(0, len(test_text) - maxlen - 1)
    generated = ''
    sentence = test_text[start_index: start_index + maxlen]
    generated += sentence
    print('----- Generating with seed: "' + sentence + '"')
    sys.stdout.write(generated)

    for i in range(400):
        x = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(sentence):
			if char not in sentence: 
				continue 
			x[0, t, char_indices[char]] = 1

        preds = model.predict(x, verbose=0)[0]
        next_index = sample(preds, diversity)
        next_char = indices_char[next_index]

        generated += next_char
        sentence = sentence[1:] + next_char

        sys.stdout.write(next_char)
        sys.stdout.flush()
    print()
'''