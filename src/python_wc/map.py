import sys

for line in sys.stdin:
    data_list = line.strip().split()
    for i in range(0, len(data_list)):
        print(data_list[i])