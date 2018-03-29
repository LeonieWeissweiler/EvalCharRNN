#!/usr/bin/python3
import sys
import numpy as np
import re
import os

plot_type = "sample"

data_dir = "../data/wikipedia/"
letters = re.compile(r'\W+')
numbers = re.compile(r'[0-9]+')
spaces = re.compile(r'\s+')

languages = [ name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name)) ]

for language in languages:
    try:
        if os.stat(data_dir + language + "/generated_wordlist.txt").st_size == 0:
            print("empty file found for", language)
            continue
        huge_dict = {}
        gen_dict = {}
        gen_file = open(data_dir + language + "/generated_wordlist.txt")
        for line in gen_file:
            word, freq = line.split(" ")
            gen_dict[word] = int(freq)
        gen_file.close()

        huge_file = open(data_dir + language + "/huge_wordlist.txt")
        for line in huge_file:
            word, freq = line.split(" ")
            huge_dict[word] = int(freq)
        huge_file.close()

        all_frequencies = list(gen_dict.values())
        biggest_freq = np.max(all_frequencies)
        good_y = np.zeros((biggest_freq+1))
        bad_y = np.zeros((biggest_freq+1))
        x = range(biggest_freq+1)

        for word, freq in gen_dict.items():
            if word in huge_dict:
                good_y[freq] += 1
            else:
                bad_y[freq] += 1

        performance_y = good_y / (good_y + bad_y)

        def write(x,y,name):
            outlist = np.array([np.array(x), np.array(y)])
            outfile = open(data_dir + language + "/" + name + "_data.npy", "wb")
            np.save(outfile, outlist)
            outfile.close()

        write(x, performance_y,"performance_freqs")

    except OSError:
        print("no generated found for", language)
