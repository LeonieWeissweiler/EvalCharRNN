#!/usr/bin/python3
import sys
import numpy as np
import os
import re

data_dir = "../data/wikipedia/"
letters = re.compile(r'\W+')
numbers = re.compile(r'[0-9]+')
spaces = re.compile(r'\s+')

def plot(filetype, model):
    languages = [ name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name)) ]
    for language in languages:
        try:
            if os.stat(data_dir + language + "/" + model + "/" + filetype + ".txt").st_size == 0:
                print("empty file found for", language)
                continue
            cdict = {}
            count_list = 0
            count_size = 0
            list_data = []
            size_data = []
            infile = open(data_dir + language + "/" + model + "/" + filetype + ".txt")
            for line in infile:
                line = line.strip()
                line = letters.sub(" ", line)
                line = numbers.sub(" ", line)
                line = spaces.sub(" ", line)
                for word in line.split(" "):
                    if word not in cdict:
                        cdict[word] = 1
                        count_list += 1
                    count_size += 1
                    if count_size % 100 == 0:
                        list_data.append(count_list)
                        size_data.append(count_size)
                        if count_size % 1000000 == 0:
                            print(language,count_size)
            infile.close()

            outlist = np.array([np.array(size_data), np.array(list_data)])

            outfile = open(data_dir + language + "/" + model + "/" + filetype + "_types_data.npy", "wb")
            np.save(outfile, outlist)
            outfile.close()

            if filetype == "huge":
                gen_wordlist_dict = {}
                gen_wordlist_file = open(data_dir + language + "/lstm/generated_wordlist.txt", "r")
                for line in gen_wordlist_file:
                    word, freq = line.split(" ")
                    gen_wordlist_dict[word] = int(freq)
                gen_wordlist_file.close()
                gen_words_total = np.sum(list(gen_wordlist_dict.values()))

                words_cut = gen_words_total // 100
                gensize_size_data = size_data[:words_cut]
                gensize_list_data = list_data[:words_cut]
                gensize_outlist = np.array([np.array(gensize_size_data), np.array(gensize_list_data)])
                gensize_outfile = open(data_dir + language + "/" + model + "/gensize_huge_types_data.npy", "wb")
                np.save(gensize_outfile, gensize_outlist)
                gensize_outfile.close()

                small_dict = {}
                small_file = open(data_dir + "el/huge_wordlist.txt", "r")
                for line in small_file:
                    word, freq = line.split(" ")
                    small_dict[word] = int(freq)
                small_file.close()

                small_count_token = np.sum(list(small_dict.values()))
                cut_token = small_count_token // 100

                small_size_data = size_data[:cut_token]
                small_list_data = list_data[:cut_token]
                small_outlist = np.array([np.array(small_size_data), np.array(small_list_data)])
                small_outfile = open(data_dir + language + "/" + model + "/small_huge_types_data.npy", "wb")
                np.save(small_outfile, small_outlist)
                small_outfile.close()

        except OSError as error:
            print(error)
            print("no file found for", language)

models = ["lstm", "rnn", "nas", "gru"]

for model in models:
    plot("generated", model)
plot("huge", "")
