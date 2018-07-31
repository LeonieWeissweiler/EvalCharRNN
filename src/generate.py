#!/usr/bin/python3
import os
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import pickle
import numpy as np
from datetime import datetime as dt
import re
from multiprocessing import Pool

languages = ["en", "fi"]# "de", "fr", "es", "ru", "cs"]
models = ["nas", "gru", "rnn", "lstm"]
sample_modes = ["0", "1", "2"] #0 to use max at each timestep, 1 to sample at each timestep, 2 to sample on spaces')
rnn_sizes = ["50", "100", "300"]
train_sizes = ["1m", "5m", "full"]
corpus = "mwc"

n_generate = "500000"
num_layers = "2"
batch_size = "50"
seq_length = "50"
num_epochs = "50"
learning_rate = "0.002"
decay_rate = "0.97"

def main(language, train_size, sample_mode, rnn_size, model):
    print(language, train_size, sample_mode, rnn_size, model)
    path = "../data/" + corpus + "/" + language + "/" + train_size + "/" + sample_mode + "/" + rnn_size + "/" + model + "/"

    if not os.stat(path + "/generated_wordlist.txt").st_size == 0:
        print("file found for", path + "/generated_wordlist.txt")
        return

    if train_size == "full":
        train_data_dir = "../data/" + corpus + "/" + language

    train_data_dir = "../data/" + corpus + "/" + language + "/" + train_size
    huge_data_dir = "../data/" + corpus + "/" + language
    save_dir = path + "save"
    log_dir = path + "logs"

    starting_time = dt.now()
    os.system("export PYTHONIOENCODING=utf-8; export CUDA_VISIBLE_DEVICES=2; python3 train.py --data_dir=" + train_data_dir + " --save_dir=" + save_dir + " --log_dir=" + log_dir + " --model=" + model + " --rnn_size=" + rnn_size + " --num_layers=" + num_layers + " --batch_size=" + batch_size + " --seq_length=" + seq_length + " --num_epochs=" + num_epochs + " --learning_rate=" + learning_rate + " --decay_rate=" + decay_rate)
    print("training time %s" % str(dt.now() - starting_time))

    starting_time = dt.now()
    os.system("export PYTHONIOENCODING=utf-8; export CUDA_VISIBLE_DEVICES=2; python3 sample.py -n=" +n_generate + " --save_dir=" + save_dir + " > " + path + "generated.txt")
    print("sampling time %s" % str(dt.now() - starting_time))

    os.system("rm -r " + log_dir)

list = [(language, train_size, sample_mode, rnn_size, model) for language in languages for train_size in train_sizes for sample_mode in sample_modes for rnn_size in rnn_sizes for model in models]

with Pool(6) as p:
    p.starmap(main, list)
