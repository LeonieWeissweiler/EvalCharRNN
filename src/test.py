import re
import sys

lang = sys.argv[1]

infile = open("../data/wikipedia/" + lang + "/huge.txt")
instring = infile.read()
infile.close()

# break_re = re.compile(r".{10}-.{10}")
# found = break_re.findall(instring)

i_re = re.compile(r"\( i \)")
found = i_re.findall(instring)
print(len(found))
