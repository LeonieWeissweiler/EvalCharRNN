#!/usr/bin/python3
import scipy.optimize
import os
import numpy as np
import sys

data_dir = "../data/wikipedia/"

def heaps_law(n,K,beta):
  return K * (n ** beta)

def fit_heaps_law(x,y):
    popt, _ = scipy.optimize.curve_fit(heaps_law,x,y)
    K = popt[0]
    beta = popt[1]
    return K,beta

def fit_filetype(filetype, model, languages):
    outfile = open("../heap/" + filetype + "_" + model + "_heap_data.txt", "w")

    for language in languages:
        try:
            path = data_dir + language + "/" + model + "/" + filetype + "_data.npy"
            print(path)
            if os.stat(path).st_size == 0:
                continue
            infile = open(path, "rb")
            data = np.load(infile)
            x = data[0]
            y = data[1]
            K, beta = fit_heaps_law(x,y)
            values_string =  "%s K=%.2f beta=%.2f\n" % (language, K, beta)
            outfile.write(values_string)

        except OSError:
            print("no file found for", language)
    outfile.close()


languages = [ name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name)) ]

models = ["lstm", "rnn", "nas", "gru"]
language_dirs = [data_dir + name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name)) ]

fit_filetype("huge_types", "", language_dirs)
filetypes = ["gen_token_type_performance", "gen_type_type_performance", "generated_types", "huge_token_type_performance", "huge_type_type_performance"]
for model in models:
    for filetype in filetypes:
        fit_filetype(filetype, model, languages)
