#!/usr/bin/python3
from nltk.tokenize import sent_tokenize
import sys

language = sys.argv[1]
infile = open(language+'.txt', 'r')
text = infile.read()
infile.close()

sentences = sent_tokenize(text)

outfile = open(language + '_sent.txt', 'w')
towrite = '\n'.join(sentences)
outfile.write(towrite)
outfile.close()
