#!/usr/bin/python3
path = "../data/mwc/"
languages = ["en", "fi", "de", "fr", "es", "ru", "cs"]
for lang in languages:
    file = open(path + lang + "/corpus.txt")
    contents = file.read()
    file.close()
    length = len(contents)
    contents1 = contents[:]
    contents2 = contents[:]
    contents3 = contents[:]
    contents4 = contents[:]
    huge = contents1[length//2:]
    print("huge", len(huge))
    one_m = contents2[:1000000]
    print("one", len(one_m))
    five_m = contents3[:5000000]
    print("five", len(five_m))
    full = contents4[:length//2]
    print("full", len(full))

    with open(path + lang + "/huge.txt", "w") as file:
        file.write(contents)

    with open(path + lang + "/1m/input.txt", "w") as file:
        file.write(one_m)

    with open(path + lang + "/5m/input.txt", "w") as file:
        file.write(five_m)

    with open(path + lang + "/full/input.txt", "w") as file:
        file.write(full)
