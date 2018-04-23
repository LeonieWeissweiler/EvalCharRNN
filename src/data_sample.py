#!/usr/bin/python3
import sys
import numpy as np
import re
import os

data_dir = "../data/wikipedia/"
letters = re.compile(r'\W+')
numbers = re.compile(r'[0-9]+')
spaces = re.compile(r'\s+')

languages = [ name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name)) ]

def plot(model):
    for language in languages:
        print(language, model)
        try:
            if os.stat(data_dir + language + "/" + model + "/generated.txt").st_size == 0:
                print("empty file found for", language)
                continue
            huge_dict = {}
            gen_file = open(data_dir + language + "/" + model + "/generated.txt")

            huge_file = open(data_dir + language + "/huge_wordlist.txt")
            for line in huge_file:
                word, freq = line.split(" ")
                huge_dict[word] = int(freq)
            huge_file.close()

            input_dict = {}
            input_file = open(data_dir + language + "/input_wordlist.txt")
            for line in input_file:
                word, freq = line.split(" ")
                input_dict[word] = int(freq)
            input_file.close()

            gen_dict = {}
            gen_type_size = 0
            gen_token_size = 0
            gen_char_size = 0
            good_token_size = 0
            new_type_size = 0
            train_token_size = 0
            train_type_size = 0
            token_x = []
            type_x = []
            char_x = []
            token_y = []
            type_y_for_token_x = []
            type_y_for_type_x = []
            train_token_y = []
            train_type_y_for_token_x = []
            train_type_y_for_type_x = []
            for line in gen_file:
                line = line.strip()
                line = letters.sub(" ", line)
                line = numbers.sub(" ", line)
                line = spaces.sub(" ", line)
                for word in line.split(" "):
                    gen_char_size += len(word) + 1
                    gen_token_size += 1
                    if word in huge_dict:
                        good_token_size += 1
                        if word not in gen_dict and word not in input_dict:
                            new_type_size += 1
                    if word in input_dict:
                        train_token_size += 1
                    if word not in gen_dict:
                        gen_dict[word] = 1
                        gen_type_size += 1
                        if word in input_dict:
                            train_type_size += 1
                        if gen_type_size % 100 == 0:
                            type_x.append(gen_type_size)
                            type_y_for_type_x.append(new_type_size)
                            train_type_y_for_type_x.append(train_type_size)
                    if gen_token_size % 100 == 0:
                        char_x.append(gen_char_size)
                        token_x.append(gen_token_size)
                        token_y.append(good_token_size/gen_token_size)
                        type_y_for_token_x.append(new_type_size)
                        train_token_y.append(train_token_size/gen_token_size)
                        train_type_y_for_token_x.append(train_type_size)

            gen_file.close()

            def write(x,y,name):
                outlist = np.array([np.array(x), np.array(y)])
                outfile = open(data_dir + language + "/" + model + "/" + name + "_data.npy", "wb")
                np.save(outfile, outlist)
                outfile.close()

            write(token_x, token_y,"gen_token_token_performance")
            write(token_x, type_y_for_token_x,"gen_token_type_performance")
            write(type_x, type_y_for_type_x,"gen_type_type_performance")

            write(char_x, token_y, "gen_char_token_performance")
            write(char_x, type_y_for_token_x, "gen_char_type_performance")

            write(token_x, train_token_y, "gen_train_token_token_performance")
            write(token_x, train_type_y_for_token_x, "gen_train_token_type_performance")
            write(type_x, train_type_y_for_type_x, "gen_train_type_type_performance")

        except OSError:
            print("no generated found for", language)

models = ["lstm", "rnn", "nas", "gru"]
for model in models:
    plot(model)
