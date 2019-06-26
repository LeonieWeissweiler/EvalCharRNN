#!/usr/bin/python3
import sys
import numpy as np
import regex
import os
from multiprocessing import Pool
import re

languages = ["en", "fi"]# "de", "fr", "es", "ru", "cs"]
models = ["nas", "gru", "rnn", "lstm"]
sample_modes = ["0", "1", "2"] #0 to use max at each timestep, 1 to sample at each timestep, 2 to sample on spaces')
rnn_sizes = ["50", "100", "300"]
train_sizes = ["1m", "5m", "full"]
metrics = ["correctness", "new_correctness"]
tokentypes = ["token", "type"]
corpus = "mwc"
letters = regex.compile(r'[^\p{L}\p{M}]')
numbers = regex.compile(r'[0-9]+')
spaces = regex.compile(r'\s+')

results_map = {} #language model samplemode (train_size, rnn_size)
for metric in metrics:
    results_map[metric] = {}
    for tokentype in tokentypes:
        results_map[metric][tokentype] = {}
        for language in languages:
            results_map[metric][tokentype][language]={}
            for model in models:
                results_map[metric][tokentype][language][model] = {}
                for sample_mode in sample_modes:
                    results_map[metric][tokentype][language][model][sample_mode] = {}
                    for train_size in train_sizes:
                        results_map[metric][tokentype][language][model][sample_mode][train_size] = {}
                        for rnn_size in rnn_sizes:
                            results_map[metric][tokentype][language][model][sample_mode][train_size][rnn_size] = 0

def main(language, train_size, sample_mode, rnn_size, model):
    path = "../data/" + corpus + "/" + language + "/" + train_size + "/" + sample_mode + "/" + rnn_size + "/" + model + "/"
    path_train = "../data/" + corpus + "/" + language + "/" + train_size + "/"
    path_huge = "../data/" + corpus + "/" + language + "/"

    gen_dict = {}
    if os.stat(path + "/generated_wordlist.txt").st_size == 0:
        print("empty file found for", path + "/generated_wordlist.txt")
        return results_map
    gen_file = open(path + "/generated_wordlist.txt")
    for line in gen_file:
        word, freq = line.split(" ")
        gen_dict[word] = int(freq)
    gen_file.close()

    huge_dict = {}
    huge_file = open(path_huge + "/huge_wordlist.txt")
    for line in huge_file:
        word, freq = line.split(" ")
        huge_dict[word] = int(freq)
    huge_file.close()

    input_dict = {}
    input_file = open(path_train + "/input_wordlist.txt")
    for line in input_file:
        word, freq = line.split(" ")
        input_dict[word] = int(freq)
    input_file.close()

    good_tokens = np.sum([gen_dict[word] if word in huge_dict else 0 for word in gen_dict.keys()]) #tokens in huge
    new_good_tokens = np.sum([gen_dict[word] if word in huge_dict and word not in input_dict else 0 for word in gen_dict.keys()]) #unique new good tokenwise
    new_tokens = np.sum([gen_dict[word] if word not in input_dict else 0 for word in gen_dict.keys()]) #unique new good and bad types

    good_types = np.sum([1 if word in huge_dict else 0 for word in gen_dict.keys()]) #types in huge
    new_good_types = np.sum([1 if word in huge_dict and word not in input_dict else 0 for word in gen_dict.keys()]) #unique new good typewise
    new_types = np.sum([1 if word not in input_dict else 0 for word in gen_dict.keys()]) #unique new good and bad types


    # percentage_regex = re.compile(r'\d{1,2}\.(\d{2})(\d{2}).*')

    correctness_percentage_token = str(good_tokens / sum(gen_dict.values())) #overall correct tokens
    # correctness_percentage_token = re.sub(percentage_regex, r'\1.\2' , correctness_percentage_token)
    correctness_percentage_type = str(good_types / len(gen_dict.values())) #overall correct types
    # correctness_percentage_type = re.sub(percentage_regex, r'\1.\2' , correctness_percentage_type)

    new_sensibleness_token = str(new_good_tokens / new_tokens) #what's good out of new tokens
    # new_sensibleness_token = re.sub(percentage_regex, r'\1.\2' , new_sensibleness_token)
    new_sensibleness_type = str(new_good_types / new_types) #what's good out of new types
    # new_sensibleness_type = re.sub(percentage_regex, r'\1.\2' , new_sensibleness_type)


    results_map["correctness"]["token"][language][model][sample_mode][train_size][rnn_size] = correctness_percentage_token
    results_map["correctness"]["type"][language][model][sample_mode][train_size][rnn_size] = correctness_percentage_type
    results_map["new_correctness"]["token"][language][model][sample_mode][train_size][rnn_size] = new_sensibleness_token
    results_map["new_correctness"]["type"][language][model][sample_mode][train_size][rnn_size] = new_sensibleness_type

    print(model, language, train_size, rnn_size, sample_mode, "token overall", correctness_percentage_token, "type overall", correctness_percentage_type,"token new", new_sensibleness_token, "type new", new_sensibleness_type)

    return results_map

list = [(language, train_size, sample_mode, rnn_size, model) for language in languages for train_size in train_sizes for sample_mode in sample_modes for rnn_size in rnn_sizes for model in models]

for model in models:
    for language in languages:
        for train_size in train_sizes:
            for rnn_size in rnn_sizes:
                for sample_mode in sample_modes:
                    main(language, train_size, sample_mode, rnn_size, model)

# main("fi", "5m", "1", "300", "gru")
