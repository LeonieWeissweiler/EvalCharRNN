#!/usr/bin/python3

n = 500000

infile = open('generated.txt', 'r', encoding="UTF-8")
text = infile.read()
infile.close()

small = text[:n]

out_small = open('generated_small.txt', 'w', encoding="UTF-8")
out_small.write(''.join(small))
out_small.close()
