#!/usr/bin/python3
import sys
from random import shuffle

n_small = int(sys.argv[1])

infile = open('huge.txt', 'r', encoding="UTF-8")
text = infile.read()
infile.close()

small = text[:n_small]

out_small = open('input.txt', 'w', encoding="UTF-8")
out_small.write(''.join(small))
out_small.close()
