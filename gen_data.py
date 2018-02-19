#!/usr/bin/python3
import sys
from random import shuffle

n_small = int(sys.argv[1])
language = sys.argv[2]

infile = open(language+'_sent.txt', 'r')
text = infile.read()
infile.close()

sentences = text.split('\n')

shuffle(sentences)

small_sentences = sentences[:n_small]

out_small = open(language + '/input.txt', 'w')
out_small.write(''.join(small_sentences))
out_small.close()
