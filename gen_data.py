#!/usr/bin/python3
from nltk.tokenize import sent_tokenize

n_small = 1
n_big = 3

infile = open('de.txt', 'r')
text = infile.read()
infile.close()

sentences = sent_tokenize(text)

if len(sentences) < n_small + n_big:
    print("not enough sentences.", len(sentences), "total sentences")
else:
    small_sentences = sentences[:n_small]
    big_sentences = sentences[-n_big:]

    out_small = open('de/input.txt', 'w')
    out_small.write(''.join(small_sentences))
    out_small.close()

    out_big = open('de/huge.txt', 'w')
    out_big.write(''.join(big_sentences))
    out_big.close()
