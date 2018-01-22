#!/usr/bin/python3
import os
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import pickle
import numpy as np

data_dir = "wikipedia/de"
save_dir = "save"
log_dir = "logs"
model = "lstm" #rnn, gru, lstm, nas
n_generate = "10000"
sample_mode = "1" #0 to use max at each timestep, 1 to sample at each timestep, 2 to sample on spaces')

os.system("python3 train.py --data_dir=data/" + data_dir + " --save_dir=" + save_dir + " --log_dir=" + log_dir + " --model=" + model)
os.system("python3 sample.py > generated.txt")

generated_dict = {}
generated = open("generated.txt", "r")
for line in generated:
    words = word_tokenize(line)
    for word in words:
        if word not in generated_dict:
            generated_dict[word] = 0
        generated_dict[word] += 1
generated.close()

train_dict = {}
train = open("data/" + data_dir + "/input.txt", "r")
for line in train:
    words = word_tokenize(line)
    for word in words:
        if word not in train_dict:
            train_dict[word] = 0
        train_dict[word] += 1
train.close()

huge_dict = {}
huge = open("data/" + data_dir + "/huge.txt", "r")
for line in huge:
    words = word_tokenize(line)
    for word in words:
        if word not in huge_dict:
            huge_dict[word] = 0
        huge_dict[word] += 1
huge.close()

generated_word_freqs = []
train_word_freqs = []
huge_word_freqs = []
for new_word, freq in generated_dict.items():
    generated_word_freqs.append(freq)
    if new_word in huge_dict:
        huge_word_freqs.append(huge_dict[new_word])
    else:
        huge_word_freqs.append(0)

    if new_word in train_dict:
        train_word_freqs.append(train_dict[new_word])
    else:
        train_word_freqs.append(0)

BINS = 100

huge_heatmap, huge_xedges, huge_yedges = np.histogram2d(generated_word_freqs, huge_word_freqs, bins=BINS)
huge_extent = [huge_xedges[0], huge_xedges[-1], huge_yedges[0], huge_yedges[-1]]

train_heatmap, train_xedges, train_yedges = np.histogram2d(generated_word_freqs, train_word_freqs, bins=BINS)
train_extent = [train_xedges[0], train_xedges[-1], train_yedges[0], train_yedges[-1]]

f, axarr = plt.subplots(2, 1, sharex=True)
f.set_size_inches((10,20))
axarr[0].set_ylabel('frequency in training corpus')
axarr[0].imshow(train_heatmap.T, extent=train_extent, aspect="auto", origin='lower')
axarr[1].set_xlabel('frequency in generated corpus')
axarr[1].set_ylabel('frequency in huge corpus')
axarr[1].imshow(huge_heatmap.T, extent=huge_extent, aspect="auto", origin='lower')
f.suptitle('Generated words with frequency in training and huge corpus')
plt.savefig('plot.pdf')
