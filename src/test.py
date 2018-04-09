import re
import sys

plot_type = sys.argv[1]

token_x_re = re.compile(r"token")
type_x_re = re.compile(r"type")
token_y_re = re.compile(r".*?\_token_performance$")
type_y_re = re.compile(r".*?\_type_performance$")

if re.match(token_x_re, plot_type):
    print("number of tokens")
elif re.match(type_x_re, plot_type):
    print("number of types")
    
if re.match(token_y_re, plot_type):
    print("sensible word percentage")
elif re.match(type_y_re, plot_type):
    print("new sensible word count")
