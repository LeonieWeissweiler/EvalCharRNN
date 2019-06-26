# !/usr/bin/python3

languages = ["en", "fi"]# "de", "fr", "es", "ru", "cs"]
models = ["nas", "gru", "rnn", "lstm"]
sample_modes = ["0", "1", "2"] #0 to use max at each timestep, 1 to sample at each timestep, 2 to sample on spaces')
rnn_sizes = ["50", "100", "300"]
train_sizes = ["1m", "5m", "full"]
metrics = ["token", "type"]
corpus = "mwc"

def main(language, train_size, sample_mode, rnn_size, model):
    path = "../data/" + corpus + "/" + language + "/" + train_size + "/" + sample_mode + "/" + rnn_size + "/" + model + "/"
    path_huge = "../data/" + corpus + "/" + language + "/"
    gen_dict = {}
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

    gen_dict_total = sum(gen_dict.values())

    length_dict = {}
    length_dict["overall"] = {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0, 8 : 0, 9 : 0, 10 : 0, 11 : 0}
    length_dict["correct"] = {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0, 8 : 0, 9 : 0, 10 : 0, 11 : 0}
    length_dict["incorrect"] = {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0, 8 : 0, 9 : 0, 10 : 0, 11 : 0}

    for word, freq in gen_dict.items():
        if len(word) > 10:
            i = 11
        else:
            i = len(word)
        length_dict["overall"][i] += freq
        if word in huge_dict:
            length_dict["correct"][i] += freq
        else:
            length_dict["incorrect"][i] += freq


    for minidict in ["overall", "correct", "incorrect"]:
        total_sum = sum(length_dict[minidict].values())
        print(language, train_size, sample_mode, rnn_size, model, total_sum, length_dict[minidict])
        for length, freq in length_dict[minidict].items():
            length_dict[minidict][length] /= total_sum
            length_dict[minidict][length] *= 100
            length_dict[minidict][length] = round(length_dict[minidict][length], 2)

    print(language, train_size, sample_mode, rnn_size, model, "overall", length_dict["overall"], "correct", length_dict["correct"], "incorrect", length_dict["incorrect"])


for model in models:
    for language in languages:
        for train_size in train_sizes:
            for rnn_size in rnn_sizes:
                for sample_mode in sample_modes:
                    main(language, train_size, sample_mode, rnn_size, model)
