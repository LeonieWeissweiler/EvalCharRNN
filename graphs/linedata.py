#!/usr/bin/python3
import re
import sys
import numpy as np

language = sys.argv[1]

cdict = {}
count_list = 0
count_size = 0
list_data = []
size_data = []
regex = re.compile(r'\w+')

infile = open("../data/wikipedia/" + language + ".txt")
for line in infile:
    for word in line.split(" "):
        if regex.match(word):
            if word not in cdict:
                cdict[word] = 1
                count_list += 1
            count_size += 1
            if count_size % 100 == 0:
                print(count_size)
                list_data.append(count_list)
                size_data.append(count_size)


infile.close()

outlist = np.array([np.array(size_data), np.array(list_data)])

outfile = open("../data/wikipedia/graphdata/" + language + "_data.npy", "wb")
np.save(outfile, outlist)
outfile.close()
