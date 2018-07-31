#!/usr/bin/python3
import sys
import numpy as np
import regex
import os

data_dir = "../data/wikipedia/"

def read(name, language, model):
	[x,y] = np.load(data_dir + language + "/" + model + "/" + name + "_data.npy")
	return (x,y)

def write(x, y, name, language, model):
    outlist = np.array([np.array(x), np.array(y)])
    outfile = open(data_dir + language + "/" + model + "/" + name + "_data.npy", "wb")
    np.save(outfile, outlist)
    outfile.close()

small_count_type = 348843
cut_type = small_count_type // 100

languages = [ name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name)) ]
models = ["lstm", "rnn", "nas", "gru"]
names = ["norm_huge_type_type_performance", "norm_huge_type_token_performance"]

for language in languages:
	for model in models:
		for name in names:
			x,y = read(name,language, model)
			x = x[:cut_type]
			y = y[:cut_type]
			write(x,y,name,language,model)