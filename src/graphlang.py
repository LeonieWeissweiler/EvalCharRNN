#!/usr/bin/python3
import numpy as np
import os
import sys
import fnmatch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

data_dir = "../data/wikipedia/"

def plot(plot_type):
    language_dirs = [ name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name)) ]
    data = {}
    captions = []

    for language in language_dirs:
        try:
            infile = open(data_dir + language + "/" + plot_type + "_data.npy", "rb")
            data[language] = np.load(infile)
            infile.close()
        except OSError:
            print("no file found for", language)

    sns.set_palette(sns.color_palette("hsv", len(data.items())))

    for language, axes in data.items():
        x = axes[0]
        y = axes[1]
        plt.plot(x,y)
        captions.append(language)


    plt.legend(captions, loc='upper right', fontsize=4)
    if plot_type == "generated_types" or plot_type == "huge_types":
        plt.xlabel("number of tokens")
        plt.ylabel("number of types")
    elif plot_type == "token_token_performance":
        plt.xlabel("Number of tokens")
        plt.ylabel("Performance (by tokens)")
    elif plot_type == "token_type_performance":
        plt.xlabel("Number of tokens")
        plt.ylabel("Performance (by types)")
    elif plot_type == "type_type_performance":
        plt.xlabel("Number of types")
        plt.ylabel("Performance (by types)")
    elif plot_type == "good_freqs":
        plt.xlabel("Word Frequency")
        plt.ylabel("Words with this frequency")
    elif plot_type == "bad_freqs":
        plt.xlabel("Word Frequency")
        plt.ylabel("Words with this frequency")
    plt.savefig("../graphs/" + plot_type + ".pdf")
    plt.clf()

if len(sys.argv) < 2:
    type_pattern = "*"
else:
    type_pattern = sys.argv[1]

language_dirs = [data_dir + name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name)) ]
types = set([name[:-len("_data.npy")] for dir in language_dirs for name in os.listdir(dir) if name.endswith("_data.npy")])
types_to_plot = [type for type in types if fnmatch.fnmatch(type,type_pattern)]
print("plotting", types_to_plot)

for type in types_to_plot:
    plot(type)
