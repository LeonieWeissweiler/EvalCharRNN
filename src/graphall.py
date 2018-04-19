#!/usr/bin/python3
import numpy as np
import os
import sys
import fnmatch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import re

data_dir = "../data/wikipedia/"
huge_re = re.compile(r"huge")
gen_re = re.compile(r"gen")
token_x_re = re.compile(r"(huge|gen)\_token")
type_x_re = re.compile(r"(huge|gen)\_type")
token_y_re = re.compile(r".*?\_token_performance$")
type_y_re = re.compile(r".*?\_type_performance$")

def plot(plot_type, model):
    print("plotting", plot_type, model)
    language_dirs = [ name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name)) ]
    data = {}
    captions = []

    for language in language_dirs:
        try:
            infile = open(data_dir + language + "/" + model + "/" + plot_type + "_data.npy", "rb")
            data[language] = np.load(infile)
            infile.close()
        except OSError:
            print("no file found for", language, model, plot_type)
            return

    sns.set_palette(sns.color_palette("hsv", len(data.items())))

    for language, axes in data.items():
        x = axes[0]
        y = axes[1]
        plt.plot(x,y)
        captions.append(language)

    x_label = ""
    y_label = ""

    plt.legend(captions, loc='upper right', fontsize=4)

    if plot_type == "generated_types":
        x_label = "number of tokens in generated"
        y_label = "number of types in generated"
    elif plot_type == "huge_types":
        x_label = "number of tokens"
        y_label = "number of types"

    if re.match(token_x_re, plot_type):
        x_label = "number of tokens"
    elif re.match(type_x_re, plot_type):
        x_label = "number of types"

    if re.match(token_y_re, plot_type):
        y_label = "sensible word percentage"
    elif re.match(type_y_re, plot_type):
        y_label = "new sensible word count"

    if re.match(huge_re, plot_type):
        x_label += " in huge"
    elif re.match(gen_re, plot_type):
        x_label += " in generated"

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.ylim(ymin=0)
    plt.xlim(xmin=0)
    plt.savefig("../graphs/" + model + "/" + plot_type + ".pdf")
    plt.clf()

if len(sys.argv) < 2:
    type_pattern = "*"
else:
    type_pattern = sys.argv[1]

language_dirs = [data_dir + name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name)) ]
types = set([name[:-len("_data.npy")] for dir in language_dirs for name in os.listdir(dir +  "/lstm") if (name.endswith("_data.npy"))])

types_without_models = ["huge_types", "gensize_huge_types", "small_huge_types"]
types_to_plot = [type for type in types if fnmatch.fnmatch(type,type_pattern)]
print("plotting", types_to_plot)

for type in types_without_models:
    print(type)
    plot(type, "")

models = ["lstm", "rnn", "nas", "gru"]
for type in types_to_plot:
    for model in models:
        plot(type, model)
