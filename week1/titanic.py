##  This is the Exercise1 for Introduction to Data Science course
##  https://www.kaggle.com/c/titanic/data
##  Univ. of Helsinki, Ege Can Ozer - 014692310

import pandas as pd
import re
import json

# 1 - Read the data using pandas
df = pd.read_csv('data/titanic_train.csv')

# 2 - Remove 'Name' column
df.drop('Name', axis=1, inplace=True) # axis=1 means drop column, 0 is for rows
df.drop('Ticket', axis=1, inplace=True)
print("Name, Ticket columns removed")

# 3 - Check the 'Cabin' column, it contains letter and number,
# get only the letter part and create a new column as 'Deck'
def cabin_letter(cabins):
    # return single letter cabins as it is
    if len(cabins) == 1: return cabins
    # A cabin contains LETTER AND NUMBER, check the passenger_id 128, F E69, ignore F
    match = re.compile("([a-zA-Z]+[0-9]+)").search(cabins)
    if match:
        one_cabin = match.group()
        # replace the number
        match = re.compile("([a-zA-Z]+)").search(one_cabin)
        if match:
            return match.group()

# Replace the non-null entries with the above function to new column Desk
df['Desk'] = df['Cabin'][df.Cabin.notnull()].map(lambda x : cabin_letter(x))
# Remove the cabin column as well
df.drop('Cabin', axis=1, inplace=True) # axis=1 means drop column, 0 is for rows
print("Cabin columns is removed")

# 5 - Impute missing values:    - Continous values      -> average of
#                               - Discrete&categorical  -> mode    of column

# Embarked, Desk, Age have missing values
df['Age'].fillna(df.Age.mean(), inplace=True)
df['Age'] = df['Age'].round() # round the age
df['Age'] = df['Age'].astype(int) # Convert floats to int

df.Embarked.fillna(df.Embarked.mode()[0], inplace=True)
df.Desk.fillna(df.Desk.mode()[0], inplace=True)
print("Filling the missing values")


# 4 - Transform categorical columns to distinct integers
# use factorize for that purpose
# EXAMPLE:
# print (df)
#        A      B      C
# 0  type1  type1  type1
# 1  type2  type2  type3
# 2  type2  type3  type3
#
# print (df.apply(lambda x: pd.factorize(x)[0]))
#    A  B  C
# 0  0  0  0
# 1  1  1  1
# 2  1  2  1
# df.apply(lambda x: pd.factorize(x)[0]) # do to whole data frame
# For some reason below generates wrong indecis
# stacked = df[['Sex', 'Embarked','Desk']].stack()
# df[['Sex', 'Embarked','Desk']] = pd.Series(stacked.factorize()[0], index=stacked.index).unstack()
df['Sex'] = pd.factorize(df['Sex'])[0]
df['Embarked'] = pd.factorize(df['Embarked'])[0]
df['Desk'] = pd.factorize(df['Desk'])[0]

print("Sex, Embarked, Desk is factorized")
# 6 - Save the all numeric containing values to .csv and then convert it to .json format
# [
#     {
#         "Deck": 0,
#         "Age": 20,
#         "Survived", 0
#         ...
#     },
#     {
#         ...
#     }
# ]
# Exclude pandas' index in csv
df.to_csv('output/titanic.csv', index=False)

# Pretty print via python's json library
df.to_json('output/temp.json', orient='records')
with open('output/temp.json') as json_data:
    d = json.load(json_data)
    with open('output/titanic.json', 'w') as json_data:
        res = json.dump(d, json_data, sort_keys=True, indent=4, separators=(',', ': '))
import os
os.remove('output/temp.json')

print("All files saved successfully under /output/ folder")
