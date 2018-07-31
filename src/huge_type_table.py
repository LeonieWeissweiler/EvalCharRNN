import sys
import numpy as np
import os


data_dir = "../data/wikipedia/"

languages = [ name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name)) ]
models = ["rnn", "lstm", "nas", "gru"]

def type_type_performance(language, model):
	path = os.path.join(data_dir, language, model, "huge_type_type_performance_data.npy")
	[x,y] = np.load(path)
	return y[-1]
	
def type_token_performance(language, model):
	path = os.path.join(data_dir, language, model, "huge_type_token_performance_data.npy")
	[x,y] = np.load(path)
	return "%.2f\\%%" % (y[-1] * 100)

for model in models:
	print("\\begin{table}[]\n\\centering\n\\caption{" + model + "}\n\\label{my-label}\n\\begin{tabular}{lrr}")
	print("\\textbf{Language} & \\textbf{New sensible word count} & \\textbf{Correctness percentage} \\\\ \\hline \\hline")
	for language in languages:
		print(language,"&",type_type_performance(language,model), "&",type_token_performance(language,model), "\\\\ \\hline")
		
	print("\\end{tabular}\n\\end{table}")
	print("\n\n\n")