#!/usr/bin/python3
from polyglot.text import Text
import os

dir = "../data/examples/"
files = os.listdir(dir)

for file in files:
    handle = open(dir + file)
    string = handle.read()
    handle.close()

    text = Text(string)
    print(file, text.language)
    tokenised = text.words

    outfile = open(dir + "tokenised_" + file, "w")
    outfile.write(" ".join(tokenised))
    outfile.close()
