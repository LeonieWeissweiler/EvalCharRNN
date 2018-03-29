#!/usr/bin/python3
import sys
from nltk.tokenize import word_tokenize

filename = sys.argv[1]
target_name = filename + "_wordlist.txt"

word_dict = {}

infile = open(filename + ".txt", "r", encoding="UTF-8")
for line in infile:
    words = word_tokenize(line)
    for word in words:
        if word not in word_dict:
            word_dict[word] = 0
        word_dict[word] += 1
infile.close()

target_file = open(target_name, "w", encoding="UTF-8")

for word, freq in word_dict.items():
    target_file.write(word + " " + str(freq) + "\n")

target_file.close()
