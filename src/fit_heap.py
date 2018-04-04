#!/usr/bin/python3
import scipy.optimize
import os
import numpy as np
import sys

def heaps_law(n,K,beta):
  return K * (n ** beta)

def fit_heaps_law(x,y,info):
    popt, _ = scipy.optimize.curve_fit(heaps_law,x,y)
    K = popt[0]
    beta = popt[1]
    return ("%s: K=%.2f beta=%.2f \n" % (info,K,beta))

def fit_filetype(filetype):
    outfile = open("../heap/" + filetype + "_heap_data.txt", "w")
    data_dir = "../data/wikipedia/"
    languages = [ name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name)) ]
    for language in languages:
        try:
            path = data_dir + language + "/" + filetype + "_data.npy"
            if os.stat(path).st_size == 0:
                continue
            infile = open(path, "rb")
            data = np.load(infile)
            x = data[0]
            y = data[1]
            values_string = fit_heaps_law(x,y,language + " " + filetype)
            outfile.write(values_string)

        except OSError:
            print("no file found for", language)
    outfile.close()


file_arg = sys.argv[1]
fit_filetype(file_arg)
