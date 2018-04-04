#!/usr/bin/python3
import scipy.optimize
import os
import numpy as np

def heaps_law(n,K,beta):
  return K * (n ** beta)

def fit_heaps_law(x,y,info):
    popt, _ = scipy.optimize.curve_fit(heaps_law,x,y)
    K = popt[0]
    beta = popt[1]
    print("%s: K=%.2f beta=%.2f" % (info,K,beta))

def fit_filetype(filetype):
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
            fit_heaps_law(x,y,language + " " + filetype)

        except OSError:
            #print("no file found for", language)



# fit_filetype("huge_types")
fit_filetype("generated_types")
