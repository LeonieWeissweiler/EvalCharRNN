#!/usr/bin/python3
import sys
import numpy as np
import re
import os

model = sys.argv[1]
data_dir = "../data/wikipedia/"
letters = re.compile(r'\W+')
numbers = re.compile(r'[0-9]+')
spaces = re.compile(r'\s+')

small_dict = {}
small_file = open(data_dir + "el/huge_wordlist.txt", "r")
for line in small_file:
    word, freq = line.split(" ")
    small_dict[word] = int(freq)
small_file.close()

small_count_token = np.sum(list(small_dict.values()))
small_count_type = len(small_dict.values())

print(small_count_token, small_count_type)

cut_token = small_count_token / 100
cut_type = small_count_type / 100

languages = [ name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name)) ]

for language in languages:
    try:
        gen_dict = {}
        huge_file = open(data_dir + language + "/huge.txt")

        if os.stat(data_dir + language + "/" + model + "/generated_wordlist.txt").st_size == 0:
            print("empty file found for", data_dir + language + "/" + model + "/generated_wordlist.txt")
            continue
        gen_file = open(data_dir + language + "/" + model + "/generated_wordlist.txt")
        for line in gen_file:
            word, freq = line.split(" ")
            gen_dict[word] = int(freq)
        gen_file.close()

        input_dict = {}
        input_file = open(data_dir + language + "/input_wordlist.txt")
        for line in input_file:
            word, freq = line.split(" ")
            input_dict[word] = int(freq)
        input_file.close()

        huge_dict = {}
        huge_type_size = 0
        huge_token_size = 0
        gen_good_tokens = 0
        gen_new_types = 0
        gen_total_tokens = sum(gen_dict.values())
        gen_total_types = len(gen_dict)
        token_x = []
        type_x = []
        token_y_for_token_x = []
        token_y_for_type_x = []
        type_y_for_token_x = []
        type_y_for_type_x = []
        for line in huge_file:
            line = line.strip()
            line = letters.sub(" ", line)
            line = numbers.sub(" ", line)
            line = spaces.sub(" ", line)
            for word in line.split(" "):
                huge_token_size += 1
                if word not in huge_dict:
                    huge_dict[word] = 1
                    huge_type_size += 1
                    if word in gen_dict:
                        gen_good_tokens += gen_dict[word]
                        if word not in input_dict:
                            gen_new_types += 1
                    if huge_type_size % 100 == 0:
                        type_x.append(huge_type_size)
                        token_y_for_type_x.append(gen_good_tokens / gen_total_tokens)
                        type_y_for_type_x.append(gen_new_types)
                if huge_token_size % 100 == 0:
                    token_x.append(huge_token_size)
                    token_y_for_token_x.append(gen_good_tokens / gen_total_tokens)
                    type_y_for_token_x.append(gen_new_types)

        gen_file.close()

        def write(x,y,name):
            outlist = np.array([np.array(x), np.array(y)])
            outfile = open(data_dir + language + "/" + model + "/" + name + "_data.npy", "wb")
            np.save(outfile, outlist)
            outfile.close()

        write(token_x, token_y_for_token_x,"huge_token_token_performance")
        write(token_x, type_y_for_token_x,"huge_token_type_performance")
        write(type_x, type_y_for_type_x,"huge_type_type_performance")
        write(type_x, token_y_for_type_x, "huge_type_token_performance")

        write(token_x[:cut_token], token_y_for_token_x[:cut_token],"norm_huge_token_token_performance")
        write(token_x[:cut_token], type_y_for_token_x[:cut_token],"norm_huge_token_type_performance")
        write(type_x[:cut_type], type_y_for_type_x[:cut_type],"norm_huge_type_type_performance")
        write(type_x[:cut_type], token_y_for_type_x[:cut_type], "norm_huge_type_token_performance")

    except OSError as error:
        print(error)
        print("no generated found for", data_dir + language + "/" + model + "/generated_wordlist.txt")
