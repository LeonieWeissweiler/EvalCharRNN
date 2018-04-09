#!/usr/bin/python3
import sys
import numpy as np
import os
import re

filetype = sys.argv[1]
model = sys.argv[2]

data_dir = "../data/wikipedia/"
letters = re.compile(r'\W+')
numbers = re.compile(r'[0-9]+')
spaces = re.compile(r'\s+')

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
    except OSError:
        print("no file found for", language)
