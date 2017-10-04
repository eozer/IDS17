import sys
word_dict = {}
for line in sys.stdin:
    v = line.strip()
    if v in word_dict:
        word_dict[v] += 1
    else:
        word_dict[v] = 1

for key in word_dict:
    print("{}\t{}".format(key, word_dict[key]))