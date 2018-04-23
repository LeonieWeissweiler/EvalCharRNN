#!/usr/bin/python3
import numpy as np
import os

least_tokens = float("inf")
smallest_lang_token = ""
least_types = float("inf")
smallest_lang_type = ""

data_dir = "../data/wikipedia/"
languages = [ name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name)) ]
models = ["lstm", "rnn", "nas", "gru"]

for language in languages:
    for model in models:
        try:
            small_dict = {}
            small_file = open(data_dir + language + "/" + model + "/generated_wordlist.txt", "r")
            for line in small_file:
                word, freq = line.split(" ")
                small_dict[word] = int(freq)
            small_file.close()
            tokens = np.sum(list(small_dict.values()))
            types = len(small_dict.values())
            if tokens < least_tokens:
                least_tokens = tokens
                smallest_lang_token = language
            if types < least_types:
                least_types = types
                smallest_lang_type = language
        except OSError:
            print("no file found for", language, model)

print(smallest_lang_token, least_tokens, smallest_lang_type, least_types)
