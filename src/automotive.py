##  This is the Exercise1 for Introduction to Data Science course
##  http://jmcauley.ucsd.edu/data/amazon/         <- Dataset
##  http://xpo6.com/download-stop-word-list/      <- Stop word list
##  Univ. of Helsinki, Ege Can Ozer - 014692310

import pandas as pd
import numpy as np
import gzip
import nltk
import re
import string

def parse(path):
    g = gzip.open(path, 'rb')
    for l in g:
        yield eval(l)


def getDF(path):
    i = 0
    df = {}
    for d in parse(path):
        df[i] = d
        i += 1
    return pd.DataFrame.from_dict(df, orient='index')

# a) Open the json file in your favorite environment, e.g python
# This is given from the given link in the comments to read into data frame
print("Reading the json data..")
df = getDF('data/reviews_Automotive_5.json.gz')

def filler(df):
    for idx, row in df.iterrows():
        if (row['reviewText'] ==  '') or (row['reviewText'] == np.nan):
            if (row['summary'] is not np.nan) or (row['summary'] != ''):
                df.loc[idx, 'reviewText'] = row['summary']
            else:
                df.loc[idx, 'reviewText'] = 'egecan'
    return df
# There are nan values inside reviewText, fill with the summary column first
# df.reviewText = df.reviewText.replace(r'\s', np.nan, regex=True)
df.reviewText = df.reviewText.fillna(df.summary)
df.reviewText = df.reviewText.fillna('')
df = filler(df)

# b) Access the reviewText field, and downcase the contents
df.reviewText = df.reviewText.map(lambda x : x.lower())

print("Reading the stop words..")
# Read stop_words and convert it to a set
stop_words = set()
with open("data/automotive_stop_words.csv") as f:
    stop_words = set(f.read().split(", "))
# Add 't' to handle this case in sanitize step, can't -> can t -> can
stop_words.add('t')
stop_words.add('s')

# TODO: Improve the punctuation remove
def sanitize(review):
    """ Sanitizes the reviewed string by removing punctuation and stop words
    :param review: review text (str)
    :return: Sanitized reviewed string
    """
    # c) Remove all punctuation, as well as the stop-words.
    # First replace punctuations with empty char then tokenize it
        # Replace punctuation with spaces using fast method
    clean = review.translate(review.maketrans(string.punctuation,
                                    ' ' * len(string.punctuation)))
    clean = re.sub(' +', ' ', clean) # remove more than 1 whitespaces
    words = nltk.word_tokenize(clean)
    # Remove stop-words
    removed_words = []
    for w in words:
        if w not in stop_words:
            removed_words.append(w)
    #removed_words = [w for w in words if w not in stop_words]
    # d) Apply a stemmer on the paragraphs, so that inflected
    # forms are mapped to the base form. For example,
    # for python the popular natural language toolkit nltk has
    # an easy-to-use stemmer.
    stemmer = nltk.stem.snowball.SnowballStemmer("english")
    res = [stemmer.stem(w) for w in removed_words]
    # Final touch join the words
    return " ".join(res)

print("Sanitizing the reviews...")
df.reviewText = df.reviewText.map(lambda x : sanitize(x))
# e) Filter the data by selecting reviews where the field
# overall is 4 or 5, and store the review texts in file pos.txt.
# Similarly, select reviews with rating 1 or 2 and store the
# reviews in file neg.txt. (Ignore the reviews with overall rating

# Filter mask for the condition
print("Filtering reviews whose overall ratings are greater than 4...")
filter = df.overall >= 4.0
filter2 = df.overall <= 2.0
pos_df = df[filter]
neg_df = df[filter2]

print("Saving files under output folder...")
pos_df.to_csv('output/pos_automotive.csv', index=False)
neg_df.to_csv('output/neg_automotive.csv', index=False)
# 3.) Each line in the two files should contain exactly one
# preprocessed review text without the rating.
# Having created two collections of positive and negative reviews,
# respectively, you may wish to take a quick look to see how the
# review texts differ between them. Here too, we will be using this
# data later to experiment with machine learning methods.
