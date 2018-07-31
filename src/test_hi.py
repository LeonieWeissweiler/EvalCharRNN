import numpy as np

language = "hi"
model = "lstm"
plot_types = ["gen_token_token_performance", "huge_token_token_performance"]
data_dir = "../data/wikipedia/"

for plot_type in plot_types:
    try:
        infile = open(data_dir + language + "/" + model + "/" + plot_type + "_data.npy", "rb")
        result = np.load(infile)
        infile.close()
        x = result[0]
        y = result[1]
        print(plot_type, np.min(x), np.max(x), np.min(y), np.max(y))
    except OSError:
        print("no file found for", language, model, plot_type)
