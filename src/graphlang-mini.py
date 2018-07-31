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
char_x_re = re.compile(r"(huge|gen|gen_train)\_char")
token_x_re = re.compile(r"(huge|gen|gen_train)\_token")
type_x_re = re.compile(r"(huge|gen|gen_train)\_type")
token_y_re = re.compile(r".*?\_token_performance$")
type_y_re = re.compile(r".*?\_type_performance$")
train_type_y_re = re.compile(r"gen_train_.*?_type_performance$")
train_token_y_re = re.compile(r"gen_train_.*?_token_performance$")

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

def format_string_for_description(description):
    if description == "rnn":
        return "k-"
    elif description == "lstm":
        return "k--"
    elif description == "gru":
        return "k-."
    elif description == "nas":
        return "k:"

    return "#666666"



def labels(plot_type):
    x_label = ""
    y_label = ""
    y_range_zero_to_one = False
    
    norm = False
    if plot_type[:5] == "norm_":
        norm = True
        plot_type = plot_type[5:]
    
    if plot_type == "generated_types" or plot_type == "huge_types" or plot_type == "small_huge_types" or plot_type == "gensize_huge_types" or plot_type == "special_token_type_ratio":
        x_label += "number of tokens"
        y_label += "number of types"

    if re.match(char_x_re, plot_type):
        x_label += "number of characters"
    elif re.match(token_x_re, plot_type):
        x_label += "number of tokens"
    elif re.match(type_x_re, plot_type):
        x_label += "number of types"

    if re.match(token_y_re, plot_type):
        y_label += "correcteness percentage"
        y_range_zero_to_one = True
    elif re.match(type_y_re, plot_type):
        y_label += "new sensible word count"

    if re.match(huge_re, plot_type):
        x_label += " in the reference data"
    if re.match(gen_re, plot_type):
        x_label += " in the generated data"
        
    if norm:
        x_label += " (scaled to length of smallest language)"
        
    return (x_label, y_label, y_range_zero_to_one)


def subplot(ax, data_dict, plot_type):
    captions = []

    for description, axes in data_dict.items():
        if axes is None:
            continue
        x = axes[0]
        y = axes[1]
        ax.plot(x,y,format_string_for_description(description))
        captions.append(description)

    x_label = ""
    y_label = ""
    ax.legend(captions, loc='upper right', fontsize=4)

    x_label, y_label, y_range_zero_to_one = labels(plot_type)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xlim(xmin=0)
    if y_range_zero_to_one:
        ax.set_ylim(ymin=0,ymax = 1)
    else:
        ax.set_ylim(ymin=0)

def own_plot(language, models):
    with PdfPages("../graphs/mini_languages/" + language + "_all_graphs.pdf") as pdf:
        print("Plotting language " + language + " with models", models)
        fig = plt.figure(figsize=((12,4)))

        # Create full subplot array
        axarr = [
            plt.subplot(1,3,1),
            plt.subplot(1,3,2),
            plt.subplot(1,3,3)
        ]
        # Replace single subplot objects to add axis sharing links
        axarr[2] = plt.subplot(1,3,3,sharex=axarr[1])

        # upper left: type-token ratios und heaps law
        data = {}
        data["huge"] = read_npy(language, "" , "huge_types")
        largest_gen_tokens = 0
        for model in models:
            data[model] = read_npy(language, model, "generated_types")
            length = len(data[model][0])
            if length > largest_gen_tokens:
                print(length)
                largest_gen_tokens = length

        data["huge"] = data["huge"][:,:largest_gen_tokens]

        subplot(axarr[0], data, "special_token_type_ratio")
        i = 1
        types = ["huge_type_token_performance", "huge_type_type_performance"]
        for typ in types:
            print("Plotting", typ)
            subplot(axarr[i], subplot_data(typ, models), typ)
            i += 1

        fig.autofmt_xdate()
        plt.tight_layout()
        pdf.savefig()
        plt.clf()


languages = [name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name))]
models = ["lstm", "rnn", "nas", "gru"]

for language in languages:
    own_plot(language, models)
