import sys

prev_key = ""

scores = ""
name = ""

active = ""
cnt = 0
# Start lines
for line in sys.stdin:
    # Process the raw
    line = line.strip() # remove \r
    key_value = line.split('|')
    key = key_value[0]
    str_values = key_value[1]
    # Init
    cnt = cnt + 1
    cur_key = key

    # What is this line
    values = str_values.split(',')
    if len(values) == 3:
        scores = " ".join(values)
        active = "scores"
    else:
        name = " ".join(values)
        active = "student"

    # Join operation
    if cnt > 1:
        if prev_key == cur_key:
            print('{} {} {}'.format(prev_key, name, scores))
            # reset fields
            scores = ""
            name = ""
    # save prev key
    prev_key = cur_key
