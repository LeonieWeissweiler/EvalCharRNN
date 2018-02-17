#!/usr/bin/python3
import os
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import pickle
import numpy as np
from datetime import datetime as dt
import sys

# language = sys.argv[1]

data_dir = "wikipedia/de/" #+ language + "/"

save_dir = "save"
log_dir = "logs"
model = "lstm" #rnn, gru, lstm, nas
n_generate = "100000"
sample_mode = "1" #0 to use max at each timestep, 1 to sample at each timestep, 2 to sample on spaces')
rnn_size = "128"
num_layers = "2"
batch_size = "50"
seq_length = "50"
num_epochs = "50"
learning_rate = "0.002"
decay_rate = "0.97"

# path = language + "_" + model

# starting_time = dt.now()
# os.system("python3 train.py --data_dir=data/" + data_dir + " --model=" + model + "--rnn_size=" + rnn_size + "--num_layers=" + num_layers + "--batch_size=" + batch_size + "--seq_length=" + seq_length + "--num_epochs=" + num_epochs + "--learning_rate=" + learning_rate + "--decay_rate=" + decay_rate)
# train_time = "training time %s" % str(dt.now() - starting_time))
#
# starting_time = dt.now()
# os.system("python3 sample.py -n=" +n_generate +"> generated.txt")
# sampling_time = "training time %s" % str(dt.now() - starting_time))

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
train = open("data/" + data_dir + "input.txt", "r")
for line in train:
    words = word_tokenize(line)
    for word in words:
        if word not in train_dict:
            train_dict[word] = 0
        train_dict[word] += 1
train.close()

huge_dict = {}
huge = open("data/" + data_dir + "huge.txt", "r")
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


BINS = 200

huge_heatmap, huge_xedges, huge_yedges = np.histogram2d(generated_word_freqs, huge_word_freqs, bins=BINS)
huge_extent = [huge_xedges[0], huge_xedges[-1], huge_yedges[0], huge_yedges[-1]]

train_heatmap, train_xedges, train_yedges = np.histogram2d(generated_word_freqs, train_word_freqs, bins=BINS)
train_extent = [train_xedges[0], train_xedges[-1], train_yedges[0], train_yedges[-1]]

train_heatmap = np.log(train_heatmap + 0.01)
huge_heatmap = np.log(huge_heatmap + 0.01)

train_percentage = 100 * np.sum([1 if x > 0 else 0 for x in train_word_freqs])/len(train_word_freqs)
huge_percentage = 100 * np.sum([1 if x > 0 else 0 for x in huge_word_freqs])/len(huge_word_freqs)

new_good_list = [1 if huge_word_freqs[x] > 0 else 0 for x in range(len(train_word_freqs)) if train_word_freqs[x] == 0]
new_good_percentage = 100 * np.sum(new_good_list) / len(new_good_list)

f, axarr = plt.subplots(2, 1, sharex=True)
f.set_size_inches((10,20))
axarr[0].set_ylabel('frequency in training corpus, percentage in train %.2f %%' % train_percentage)
axarr[0].imshow(train_heatmap.T, extent=train_extent, aspect="auto", origin='lower')
axarr[1].set_xlabel('frequency in generated corpus')
axarr[1].set_ylabel('frequency in huge corpus, percentage in huge %.2f %%' % huge_percentage)
axarr[1].imshow(huge_heatmap.T, extent=huge_extent, aspect="auto", origin='lower')
f.suptitle('Generated words with frequency in training and huge corpus')
plt.savefig('plot.pdf')

saves = open("picklesaves.pickle", "wb")
pickle.dump(generated_word_freqs, saves)
pickle.dump(train_word_freqs, saves)
pickle.dump(huge_word_freqs, saves)
saves.close()

print('Percentage of words not present in training corpus that are present in the bigger corpus: %.2f %%' % new_good_percentage)
