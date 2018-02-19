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
regex = re.compile(r'[A-Za-z]')

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

path = language + "/" #+ "_" + model

data_dir = "wikipedia/" + language + "/"
save_dir = path + "save"
log_dir = path + "logs"

starting_time = dt.now()
os.system("python3 train.py --init_from=en/save --data_dir=data/" + data_dir + " --save_dir=" + save_dir + " --log_dir=" + log_dir + " --model=" + model + " --rnn_size=" + rnn_size + " --num_layers=" + num_layers + " --batch_size=" + batch_size + " --seq_length=" + seq_length + " --num_epochs=" + num_epochs + " --learning_rate=" + learning_rate + " --decay_rate=" + decay_rate)
print("training time %s" % str(dt.now() - starting_time))

starting_time = dt.now()
os.system("python3 sample.py -n=" +n_generate + " --save_dir=" + save_dir + "> " + path + "generated.txt")
print("sampling time %s" % str(dt.now() - starting_time))

generated_dict = {}
generated = open(path + "generated.txt", "r")
for line in generated:
    words = word_tokenize(line)
    for word in words:
        if regex.search(word):
            if word not in generated_dict:
                generated_dict[word] = 0
            generated_dict[word] += 1
generated.close()

train_dict = {}
train = open("data/" + data_dir + "input_wordlist.txt", "r")
for line in train:
    line = line.strip()
    (word,freq) = line.split(" ")
    train_dict[word] = int(freq)
train.close()

huge_dict = {}
huge = open("data/" + data_dir + "huge_wordlist.txt", "r")
for line in huge:
    line = line.strip()
    (word,freq) = line.split(" ")
    huge_dict[word] = int(freq)
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

train_heatmap = np.log(train_heatmap + 0.01)
huge_heatmap = np.log(huge_heatmap + 0.01)

train_percentage_type = 100 * np.sum([1 if x > 0 else 0 for x in train_word_freqs])/len(train_word_freqs)
huge_percentage_type = 100 * np.sum([1 if x > 0 else 0 for x in huge_word_freqs])/len(huge_word_freqs)

new_good_list_type = [1 if huge_word_freqs[x] > 0 else 0 for x in range(len(train_word_freqs)) if train_word_freqs[x] == 0]
new_good_percentage_type = 100 * np.sum(new_good_list_type) / len(new_good_list_type)

train_percentage_token = 100 * np.sum([generated_word_freqs[x] if train_word_freqs[x] > 0 else 0 for x in range(len(train_word_freqs))])/np.sum(generated_word_freqs)
huge_percentage_token = 100 * np.sum([generated_word_freqs[x] if huge_word_freqs[x] > 0 else 0 for x in range(len(huge_word_freqs))])/np.sum(generated_word_freqs)

new_good_list_token = [generated_word_freqs[x] if huge_word_freqs[x] > 0 else 0 for x in range(len(train_word_freqs)) if train_word_freqs[x] == 0]
new_good_divide_list_token = [generated_word_freqs[x] for x in range(len(train_word_freqs)) if train_word_freqs[x] == 0]
new_good_percentage_token = 100 * np.sum(new_good_list_token) / np.sum(new_good_divide_list_token)

f, axarr = plt.subplots(2, 1, sharex=True)
f.set_size_inches((10,20))
axarr[0].set_ylabel('frequency in training corpus')
axarr[0].imshow(train_heatmap.T, extent=train_extent, aspect="auto", origin='lower')
axarr[1].set_xlabel('frequency in generated corpus')
axarr[1].set_ylabel('frequency in huge corpus')
axarr[1].imshow(huge_heatmap.T, extent=huge_extent, aspect="auto", origin='lower')
f.suptitle('Generated words with frequency in training and huge corpus')

f.text(0.1, 0.05, 'percentage in train, token: %.2f %% , type: %.2f %%\npercentage in huge, token: %.2f %% , type: %.2f %%\nPercentage of new words present in huge: token: %.2f %% , type: %.2f %%' % (train_percentage_token, train_percentage_type, huge_percentage_token, huge_percentage_type, new_good_percentage_token, new_good_percentage_type), fontsize=12)

plt.savefig(path + 'plot.pdf')

saves = open(path + "picklesaves.pickle", "wb")
pickle.dump(generated_word_freqs, saves)
pickle.dump(train_word_freqs, saves)
pickle.dump(huge_word_freqs, saves)
saves.close()
