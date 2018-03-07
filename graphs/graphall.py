#!/usr/bin/python3
import numpy as np
import os
import matplotlib.pyplot as plt

files = os.listdir("../data/wikipedia/graphdata/")
languages = [name[:-9] for name in files if name[-9:] == "_data.npy"]

data = {}
captions = []

# plt.set_size_inches(20,20)

for language in languages:
    infile = open("../data/wikipedia/graphdata/" + language + "_data.npy", "rb")
    data[language] = np.load(infile)
    infile.close()

for language, axes in data.items():
    x = axes[0]
    y = axes[1]
    plt.plot(x,y)
    captions.append(language)

plt.legend(captions, loc='upper left')
plt.xlabel("number of tokens")
plt.ylabel("number of types")
plt.savefig("plotall.pdf")
