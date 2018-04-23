#!/usr/bin/python3
import numpy as np
import re
import os
import sys
import fnmatch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

data_dir = "../data/wikipedia/"
heap_dir = "../heap/"
huge_re = re.compile(r"huge")
gen_re = re.compile(r"gen")
token_x_re = re.compile(r"(huge|gen)\_token")
type_x_re = re.compile(r"(huge|gen)\_type")
token_y_re = re.compile(r".*?\_token_performance$")
type_y_re = re.compile(r".*?\_type_performance$")

def subplot_data(type, models):
    data = {}
    for model in models:
        data[model] = read_npy(language, model, type)
    return data

def read_npy(language, model, plot_type):
    try:
        infile = open(data_dir + language + "/" + model + "/" + plot_type + "_data.npy", "rb")
        result = np.load(infile)
        infile.close()
        return result
    except OSError:
        print("no file found for", language, model, plot_type)

def subplot(ax, data_dict, plot_type):
    captions = []

    for description, axes in data_dict.items():
        if axes is None:
            continue
        x = axes[0]
        y = axes[1]
        ax.plot(x,y)
        captions.append(description)

    x_label = ""
    y_label = ""
    ax.legend(captions, loc='upper right', fontsize=4)

    if plot_type == "special_token_type_ratio":
        xlabel = "number of tokens"
        ylabel = "number of types"

    if re.match(token_x_re, plot_type):
        xlabel = "number of tokens"
    elif re.match(type_x_re, plot_type):
        xlabel = "number of types"

    if re.match(token_y_re, plot_type):
        ylabel = "sensible word percentage"
        ax.set_ylim(ymax=1)
    elif re.match(type_y_re, plot_type):
        ylabel = "new sensible word count"

    if re.match(huge_re, plot_type):
        xlabel += " in huge"
    elif re.match(gen_re, plot_type):
        xlabel += " in generated"

    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

def own_plot(language, models):
    print("Plotting language " + language + " with models", models)
    plt.figure(figsize=((8.27,11.96)))

    # Create full subplot array
    axarr = [
        [
            plt.subplot(4,2,1),
            plt.subplot(4,2,2)
        ],
        [
            plt.subplot(4,2,3),
            plt.subplot(4,2,4)
        ],
        [
            plt.subplot(4,2,5),
            plt.subplot(4,2,6)
        ],
        [
            plt.subplot(4,2,7),
            plt.subplot(4,2,8)
        ],
    ]
    # Replace single subplot objects to add axis sharing links
    axarr[2][1] = plt.subplot(4,2,6,sharey=axarr[2][0])
    axarr[3][0] = plt.subplot(4,2,7,sharex=axarr[2][0])
    axarr[3][1] = plt.subplot(4,2,8,sharex=axarr[2][1], sharey=axarr[3][0])

    # upper left: type-token ratios und heaps law
    data = {}
    data["huge"] = read_npy(language, "" , "gensize_huge_types")
    end = data["huge"][0][-1]
    for model in models:
        data["generated " + model] = read_npy(language, model, "generated_types")
    subplot(axarr[0][0], data, "special_token_type_ratio")
    i = 1
    types = ["gen_type_type_performance", "gen_token_token_performance", "gen_token_type_performance", "huge_type_token_performance", "huge_token_token_performance", "huge_type_type_performance", "huge_token_type_performance"]
    for typ in types:
        print("Plotting", typ)
        subplot(axarr[(i // 2)][(i % 2)], subplot_data(typ, models), typ)
        i += 1

    plt.tight_layout()
    plt.savefig("../graphs/languages/" + language + "_all_graphs.pdf")
    plt.clf()


languages = [name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name))]
models = ["lstm", "rnn", "nas", "gru"]

for language in languages:
    own_plot(language, models)
