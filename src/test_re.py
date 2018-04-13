import regex
import os
import sys

letters = regex.compile(r'[^\p{L}\p{M}]')
numbers = regex.compile(r'[0-9]')
spaces = regex.compile(r'\s+')

data_dir = "../data/wikipedia/"

lang = sys.argv[1]

inputfile = open(data_dir + lang + "/input.txt")
for line in inputfile:
    re_line = regex.sub(letters, " ", line)
    re_line = regex.sub(numbers, "0", re_line)
    re_line = regex.sub(spaces, " ", re_line)
    print(line)
    print(re_line)
    print("------")

inputfile.close()
