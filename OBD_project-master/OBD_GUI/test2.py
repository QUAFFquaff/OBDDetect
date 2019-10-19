import numpy as np


def read_txt_score1():
    with open('scores00.txt', 'r') as f:
        lines = f.readlines()
    file_list = []
    print(len(lines))
    for line in lines:

        line = line.split('[')[-1].split(']')[0]
        print(line)
        pattern_list = []
        patterns = line.split(",")
        for i in range(len(patterns)):
            # if i % 2 != 0:
            pattern_list.append(patterns[i])
        file_list.append(pattern_list)
    return file_list

print(read_txt_score1())