#!/usr/bin/python3
import sys
from random import shuffle

n_small = int(sys.argv[1])
n_big = int(sys.argv[2])
language = sys.argv[3]

infile = open(language+'_sent.txt', 'r')
text = infile.read()
infile.close()

sentences = text.split('\n')

if n_small + n_big > len(sentences):
    print("not enough data")
    exit()

shuffle(sentences)

small_sentences = sentences[:n_small]
big_sentences = sentences[-n_big:]

out_small = open('de/input.txt', 'w')
out_small.write(''.join(small_sentences))
out_small.close()

out_big = open('de/huge.txt', 'w')
out_big.write(''.join(big_sentences))
out_big.close()
