#!/usr/bin/python3
import os
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import pickle
import numpy as np
from datetime import datetime as dt
import sys
import re

language = sys.argv[1]

model = "lstm" #rnn, gru, lstm, nas
n_generate = "500000"
sample_mode = "1" #0 to use max at each timestep, 1 to sample at each timestep, 2 to sample on spaces')
rnn_size = "128"
num_layers = "2"
batch_size = "50"
seq_length = "50"
num_epochs = "50"
learning_rate = "0.002"
decay_rate = "0.97"

path = "data/wikipedia/" + language + "/" + model + "/"

data_dir = "data/wikipedia/" + language + "/"
save_dir = path + "save"
log_dir = path + "logs"

starting_time = dt.now()
os.system("export PYTHONIOENCODING=utf-8; python3 src/train.py --data_dir=" + data_dir + " --save_dir=" + save_dir + " --log_dir=" + log_dir + " --model=" + model + " --rnn_size=" + rnn_size + " --num_layers=" + num_layers + " --batch_size=" + batch_size + " --seq_length=" + seq_length + " --num_epochs=" + num_epochs + " --learning_rate=" + learning_rate + " --decay_rate=" + decay_rate)
print("training time %s" % str(dt.now() - starting_time))

starting_time = dt.now()
os.system("export PYTHONIOENCODING=utf-8; python3 src/sample.py -n=" +n_generate + " --save_dir=" + save_dir + " > " + path + "generated.txt")
print("sampling time %s" % str(dt.now() - starting_time))
