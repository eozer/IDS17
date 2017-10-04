import sys

for line in sys.stdin:
    line = line.strip() # strip the \r
    line = line.split(",") # split the whole line into data fields
    key = line[0] # key-student id is always the first value
    list_values = line[1:] # get the rest the values into a list
    values = ",".join(list_values)
    # We dont need to calculate something specific to files
    # So just send it to the reducer
    print("{}|{}".format(key, values))
