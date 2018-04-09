#!/usr/bin/python3

import os
import sys

data_dir = "../data/wikipedia/"
languages = ["de", "en"]
models = ["rnn", "lstm"]

def read_wordlist(path):
	try:
		infile = open(path,"r")
		result = {line.split(" ")[0] for line in infile}
		infile.close()
		return result

	except OSError:
		print("Failed to open for wordlist creation",path)


def create_examples(language,model):
	generated_path = data_dir + language + "/" + model + "/generated_wordlist.txt"
	huge_path = data_dir + language + "/huge_wordlist.txt"
	input_path = data_dir + language + "/input_wordlist.txt"

	huge_words = read_wordlist(huge_path)
	input_words = read_wordlist(input_path)

	generated_file = open(generated_path, "r")

	huge_file = open(data_dir + language + "/" + model + "/generated_hugewords.txt", "w")
	input_file = open(data_dir + language + "/" + model + "/generated_inputwords.txt", "w")
	new_file = open(data_dir + language + "/" + model + "/generated_newwords.txt", "w")

	gendict = {}
	for line in generated_file:
		word = line.split(" ")[0]
		frequency = int(line.split(" ")[1])
		gendict[word] = frequency

	generated_file.close()

	for word,freq in sorted(gendict.items(), key=lambda x: x[1], reverse=True):
		if word in input_words:
			input_file.write(word + " " + str(freq) + "\n")
		elif word in huge_words:
			huge_file.write(word + " " + str(freq) + "\n")
		else:
			new_file.write(word + " " + str(freq) + "\n")

	huge_file.close()
	input_file.close()
	new_file.close()

for language in languages:
	for model in models:
		create_examples(language,model)
