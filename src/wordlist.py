#!/usr/bin/python3
import sys
import regex
import os
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import pickle
import numpy as np
from datetime import datetime as dt
import re
from multiprocessing import Pool

data_dir = "../data/"

letters = regex.compile(r'[^\p{L}\p{M}]')
numbers = regex.compile(r'[0-9]+')
spaces = regex.compile(r'\s+')

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

def do_wordlist(source, target):
    word_dict = {}
    infile = open(source, "r", encoding="UTF-8")
    for line in infile:
        line = line.strip()
        line = regex.sub(letters, " ", line)
        line = regex.sub(numbers, "0", line)
        line = regex.sub(spaces, " ", line)
        for word in line.split(" "):
            if word not in word_dict:
                word_dict[word] = 0
            word_dict[word] += 1
    infile.close()

    target_file = open(target, "w", encoding="UTF-8")

    for word, freq in word_dict.items():
        target_file.write(word + " " + str(freq) + "\n")

    target_file.close()


def main(language, train_size, sample_mode, rnn_size, model):
    print(language, train_size, sample_mode, rnn_size, model)
    path = os.path.join(data_dir, corpus, language, train_size, sample_mode, rnn_size, model)
    
    do_wordlist(path + "/generated.txt", path + "/generated_wordlist.txt")
    
    
    

for language in languages:
    print(language)
    lang_dir = os.path.join(data_dir, corpus, language)
    do_wordlist(lang_dir + "/huge.txt", lang_dir + "/huge_wordlist.txt")
    
    for train_size in train_sizes:
        print(train_size)
        if train_size != "full":
            train_dir = os.path.join(data_dir, corpus, language, train_size)
            do_wordlist(train_dir + "/input.txt", train_dir + "/input_wordlist.txt")


list = [(language, train_size, sample_mode, rnn_size, model) for language in languages for train_size in train_sizes for sample_mode in sample_modes for rnn_size in rnn_sizes for model in models]

with Pool(6) as p:
    p.starmap(main, list)
