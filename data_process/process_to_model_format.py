import numpy as np
import operator
from collections import OrderedDict
from operator import itemgetter

def get_vocabulary(path):
    vocabulary = []

def generate_model_data(dir, project_name, path, ratio):
    vocabulary = []
    data = open(path).read().split("ForNewFile35214")
    data_len = len(data)
    train_len = (int)(np.floor(data_len * ratio/100.0))# 90% for training, 10% for testing
    train_data = ""
    test_data = ""

    for i in range(0, train_len):
        train_data = train_data + data[i]+ " ForNewFile35214 "

    for j in range(train_len, data_len):
        test_data = test_data + data[j] + " ForNewFile35214 "
    #generate vocabulary
    #words = "apple banana apple strawberry banana lemon"
    ttf_map = reduce(lambda d, c: d.update([(c, d.get(c, 0) + 1)]) or d, train_data.split(), {})
    #print ttf_map
    ttf_cutoff = 3
    for key, value in sorted(ttf_map.iteritems(), key=lambda (k, v): (v, k), reverse= True):
        #print "%s: %s" % (key, value)
        if value > ttf_cutoff:
            vocabulary.append(key)

    vocab_file = open(dir+"/vocabulary.txt", "w")

    for i in range(0, len(vocabulary)):
        vocab_file.write(vocabulary[i]+"\n")
    vocab_file.close()

    train_file = open(dir +"/train.txt", "w")
    train_data_list = train_data.split()
    for i in range(0, len(train_data_list)):
        if train_data_list[i] in vocabulary:
            train_file.write(train_data_list[i]+" ")
        else:
            train_file.write("unknown ")
    train_file.close()

    test_file = open(dir +"/test.txt", "w")
    test_data_list = test_data.split()
    for i in range(0, len(test_data_list)):
        if test_data_list[i] in vocabulary:
            test_file.write(test_data_list[i] + " ")
        else:
            test_file.write("unknown ")
    test_file.close()


def main():
    project_name = "maven"
    work_dir = "K:/Masud/PythonProjects/dataset/autocode_data/model_data/"+project_name

    data_path = work_dir+ "/processed_code.txt"
    generate_model_data(work_dir, project_name, data_path, ratio=90)

if __name__ == "__main__":
    main()