#!/usr/bin/python3
import numpy as np
import re
import os
import sys
import fnmatch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

data_dir = "../data/wikipedia/"
heap_dir = "../heap/"
model = "lstm"
huge_re = re.compile(r"huge")
gen_re = re.compile(r"gen")
token_x_re = re.compile(r"(huge|gen)\_token")
type_y_re = re.compile(r"(huge|gen)\_type")
token_y_re = re.compile(r".*?\_token_performance$")
type_y_re = re.compile(r".*?\_type_performance$")

def subplot_data(type, models):
    data = {}
    for model in models:
        data["generated " + model] = read_npy(language, model, type)

def execute_heaps_law(K,beta,end,step):
    def heaps_law(n,K,beta):
      return K * (n ** beta)

    x = []
    y = []
    for i in range(0,end,step):
        x.append(x)
        y.append(heaps_law(i,K,beta))

    return x,y

def read_heap_params(language, model, plot_type):
    path = heap_dir + plot_type + "_" + model + "_heap_data.txt"
    infile = open(path, "r")
    result = {}

    for line in infile:
        split = line.split(" ")
        read_language = split[0]
        K = float(split[1][2:])
        beta = float(split[2][5:])
        if language == read_language:
            return (K,beta)

    print(language + " not found in " + path)

def read_npy(language, model, plot_type):
    try:
        infile = open(data_dir + language + "/" + model + "/" + plot_type + "_data.npy", "rb")
        result = np.load(infile)
        infile.close()
        return result
    except OSError:
        print("no file found for", language, plot_type)
        #DO SOMETHING

def subplot(ax, data_dict, plot_type):

    sns.set_palette(sns.color_palette("hsv", len(data_dict)))
    captions = []
    for description, axes in data_dict.items():
        x = axes[0]
        y = axes[1]
        ax.plot(x,y)
        captions.append(description)

    x_label = ""
    y_label = ""

    ax.legend(captions, loc='upper right', fontsize=4)

    if plot_type == "generated_types":
        xlabel = "number of tokens in generated"
        ylabel = "number of types in generated"
    elif plot_type == "huge_types":
        xlabel = "number of tokens"
        ylabel = "number of types"

    if re.match(token_x_re, plot_type):
        xlabel = "number of tokens"
    elif re.match(type_x_re, plot_type):
        xlabel = "number of types"

    if re.match(token_y_re, plot_type):
        ylabel = "sensible word percentage"
    elif re.match(type_y_re, plot_type):
        ylabel = "new sensible word count"

    if re.match(huge_re, plot_type):
        xlabel += " in huge"
    elif re.match(gen_re, plot_type):
        xlabel += " in generated"

    ax.xlabel(xlabel)
    ax.ylabel(ylabel)

def plot(language, models):
    print("Plotting language " + language + " with models", models)
    f, axarr = plt.subplots(2, 4)
    f.set_size_inches((8.27,11.96))

    # upper left: type-token ratios und heaps law
    print("Plotting Upper left")
    data = {}
    data["huge"] = read_npy(language, "" , "huge_types")
    end = data["huge"][0][-1]
    K,beta = read_heap_params(language, "" , "huge_types")
    data["huge (heaps approximation)"] = execute_heaps_law(K,beta,end,100)
    for model in models:
        print(model)
        data["generated " + model] = read_npy(language, model, "generated_types")
        K,beta = read_heap_params(language, model, "generated_types")
        data["generated " + model + " (heaps approximation)"] = execute_heaps_law(K,beta,end,100)
    subplot(axarr[0][0], data, "huge_types")

    i = 1
    types = ["gen_type_type_performance", "gen_token_token_performance", "gen_token_type_performance", "huge_type_token_performance", "huge_type_type_performance", "huge_token_token_performance", "huge_token_type_performance"]
    for typ in types: 
        print("Plotting", typ)
        subplot(axarr[i % 2][i / 2], subplot_data(typ, models), typ)
        i += 1

    plt.savefig("../graphs/" + language + "_all_graphs.pdf")
    plt.clf()


languages = [name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name))]
models = ["lstm"]

for language in languages:
    plot(language, models)
