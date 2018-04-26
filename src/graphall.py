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
token_x_re = re.compile(r"(huge|gen|gen_train)\_token")
type_x_re = re.compile(r"(huge|gen|gen_train)\_type")
token_y_re = re.compile(r".*?\_token_performance$")
type_y_re = re.compile(r".*?\_type_performance$")
train_type_y_re = re.compile(r"gen_train_.*?_type_performance$")
train_token_y_re = re.compile(r"gen_train_.*?_token_performance$")

fam_green_colours = set(["en", "de", "ru", "fr", "es", "it", "nl", "pl", "pt", "uk", "sv", "ca", "bg", "cs", "no", "fa", "sr", "hi", "ro", "da", "hr", "lt", "sl", "sk", "lv", "el"])
fam_blue_colours = set(["ja", "hu", "fi", "ko", "tr", "et"])
fam_red_colours = set(["zh", "vi", "id", "th", "ms"])
fam_black_colours = set(["he", "ar"])

script_green_colours = set(["en", "de", "fr", "es", "it", "nl", "pl", "pt", "sv", "ca", "hu", "cs", "fi", "no", "vi", "tr", "id", "ro", "da", "hr", "lt", "sl", "sk", "et", "lv", "ms"])
script_blue_colours = set(["ru", "uk", "bg", "sr"])
script_red_colours = set(["ar", "fa"])

colours = ["r", "g", "b", "k", "c", "m", "y"]
own_dashes = [(None, None), [2,2], [1,1], [3,3], [3,1,1,1], [2,1,1,1,1,1]] #[5,2], [10,3], [6,3,2,3], [5,2,5,2,2,2], [5,3,1,3,1,3], [10,5,5,5], [3,2,1,2]]

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

    i = 0
    for language, axes in data.items():
        x = axes[0]
        y = axes[1]
        colour = colours[i//6]
        dash = own_dashes[i%6]
        plt.plot(x,y, color=colour, dashes=dash)
        captions.append(language)
        i += 1

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

    if re.match(train_token_y_re, plot_type):
        y_label = "train word percentage (token)"
    elif re.match(train_type_y_re, plot_type):
        y_label = "train word percentage (ype)"
    elif re.match(token_y_re, plot_type):
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

def special_plot(plot_type, model, special_type):
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

    for language, axes in data.items():
        x = axes[0]
        y = axes[1]
        if special_type == "families":
            if language in fam_green_colours:
                plt.plot(x, y, "g")
            elif language in fam_red_colours:
                plt.plot(x, y, "r")
            elif language in fam_blue_colours:
                plt.plot(x, y, "b")
            elif language in fam_black_colours:
                plt.plot(x, y, "k")
            else:
                print("fail" + language)
        else:
            if language in script_green_colours:
                plt.plot(x, y, "g")
            elif language in script_red_colours:
                plt.plot(x, y, "r")
            elif language in script_blue_colours:
                plt.plot(x, y, "b")
            else:
                plt.plot(x, y, "k")
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

    if re.match(train_token_y_re, plot_type):
        y_label = "train word percentage (token)"
    elif re.match(train_type_y_re, plot_type):
        y_label = "train word percentage (ype)"
    elif re.match(token_y_re, plot_type):
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
    plt.savefig("../graphs/" + model + "/" + special_type + "/" + plot_type + ".pdf")
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
special_types = ["families", "scripts"]
for type in types_to_plot:
    for model in models:
        plot(type, model)
        for special_type in special_types:
            special_plot(type, model, special_type)

#{'marker': None, 'dash': (None,None)}
