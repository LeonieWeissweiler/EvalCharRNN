#!/usr/bin/python3

languages = ["en", "fi", "de", "fr", "es", "ru", "cs"]
path = "data/mwc/"
for language in languages:

    infile = open(path + language + '/huge.txt', 'r', encoding="UTF-8")
    text = infile.read()
    infile.close()

    small_1m = text[:1000000]
    small_5m = text[:5000000]

    out_small1 = open(path + language + '/1m/input.txt', 'w', encoding="UTF-8")
    out_small1.write(''.join(small_1m))
    out_small1.close()

    out_small5 = open(path + language + '/5m/input.txt', 'w', encoding="UTF-8")
    out_small5.write(''.join(small_5m))
    out_small5.close()
