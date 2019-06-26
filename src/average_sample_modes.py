#!/usr/bin/python3
import re
#nas en 1m 50 0 token overall 63.40 type overall 13.71 token new 07.19 type new 05.22
infile = open("../quick_results.txt")
outfile = open("../quick_results_avg.txt", "w")
token_overall_sum = 0
type_overall_sum = 0
token_new_sum = 0
type_new_sum = 0
my_re = re.compile(r'(.*?) (\d) token overall (0+.\d*?) type overall (0+.\d*?) token new (0+.\d*?) type new (0+.\d*?)\n')
short_re = re.compile(r'\d{1,2}\.(\d{2})(\d{2}).*')
for line in infile:
    match = my_re.match(line)
    rest = match.group(1)
    sample_mode = match.group(2)
    token_overall_value = float(match.group(3))
    type_overall_value = float(match.group(4))
    token_new_value = float(match.group(5))
    type_new_value = float(match.group(6))

    if token_overall_value==0 and type_overall_value==0 and token_new_value==0 and type_new_value==0:
        outfile.write(rest + " ERROR\n")

    if sample_mode == "0":
        token_overall_sum = token_overall_value
        type_overall_sum = type_overall_value
        token_new_sum = token_new_value
        type_new_sum = type_new_value
    elif sample_mode == "1":
        token_overall_sum += token_overall_value
        type_overall_sum += type_overall_value
        token_new_sum += token_new_value
        type_new_sum += type_new_value
    elif sample_mode == "2":
        token_overall_sum += token_overall_value
        type_overall_sum += type_overall_value
        token_new_sum += token_new_value
        type_new_sum += type_new_value

        token_overall_sum /= 3
        type_overall_sum /= 3
        token_new_sum /= 3
        type_new_sum /= 3

        token_overall_sum *= 100
        type_overall_sum *= 100
        token_new_sum *= 100
        type_new_sum *= 100

        token_overall_sum = round(token_overall_sum, 2)
        type_overall_sum = round(type_overall_sum, 2)
        token_new_sum = round(token_new_sum, 2)
        type_new_sum = round(type_new_sum, 2)

        token_overall_sum = str(token_overall_sum).zfill(5)
        type_overall_sum = str(type_overall_sum).zfill(5)
        token_new_sum = str(token_new_sum).zfill(5)
        type_new_sum = str(type_new_sum).zfill(5)

        outstring = rest + " token overall " + str(token_overall_sum) + " type overall " + str(type_overall_sum) + " token new " + str(token_new_sum) + " type new " + str(type_new_sum)
        print(outstring)
        outfile.write(outstring + "\n")

infile.close()
outfile.close()
