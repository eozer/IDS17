# coding: utf-8
from datetime import datetime
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

class TfIdf:
    def __init__(self):
        self.docs = []
        self.matrix = None

    def add_document(self, df, name):
        col_name = name + '_f'
        doc = {col_name: {}, 'nt': {}}
        for item in df.iteritems():
            idx, review_str = item
            review_set = list(review_str.split(' '))
            # Calculate the term frequency here, simply increment it: check tfidf weighting scheme 2
            for w in review_set:
                doc[col_name][w] = doc[col_name].get(w, 0.0) + 1.0
                doc['nt'][w] = doc['nt'].get(w, 1.0)
        df = pd.DataFrame(doc)
        df.index.name = 'term'
        df = df.reset_index()
        # save it to the list
        self.docs.append(df)

    def concat_documents(self):
        # merged = self.docs[0].merge(self.docs[1], how='outer', on='term')
        concatenated = pd.concat(self.docs)
        grouped = concatenated.groupby(['term'], as_index=False)
        self.matrix = grouped.agg(np.sum)
        self.matrix.fillna(1.0, axis=1, inplace=True)

    def calculate(self, scheme=2):
        def _tfidf(row, c, sch):
            if sch == 1:
                max_f = float(self.matrix.nlargest(1, c+'_f')[c+'_f'])
                return _tfidf1(row, c, max_f)
            elif sch == 2:
                return _tfidf2(row, c)
            else:
                return _tfidf3(row, c)

        def _tfidf1(row, c, max_f):
            idf = (0.5 + (0.5 * (row[c+'_f'] / max_f))) * math.log((len(self.docs) / (1 + row['nt'])))
            tf = (row[c+'_f'] * math.log((len(self.docs) / (1 + row['nt']))))
            res = tf * idf
            return res

        def _tfidf2(row, c):
            idf = math.log(1 + (len(self.docs) / (1 + row['nt'])))
            tf = 1 + math.log10(row[c + '_f'])
            res = tf * idf
            return res

        def _tfidf3(row, c):
            idf = math.log((len(self.docs) / (1 + row['nt']))) * (1 + math.log10(row[c + '_f']))
            tf = (math.log((len(self.docs) / (1 + row['nt'])))  * (1 + math.log10(row[c + '_f'])))
            res =  tf * idf
            return res

        self.matrix['p_tfidf'] = self.matrix.apply(lambda x : _tfidf(x, 'p', scheme), axis=1)
        self.matrix['n_tfidf'] = self.matrix.apply(lambda x: _tfidf(x, 'n', scheme), axis=1)

    def get_result(self):
        return self.matrix[['term', 'p_tfidf', 'n_tfidf']]

    def plot(self, df, c, title, color):
        y_pos = np.arange(len(df.term))
        plt.bar(y_pos, df[c], align='center', alpha=0.5, color=color)
        plt.xticks(y_pos, df.term)
        plt.ylabel('Words')
        plt.title(title)

startTime = datetime.now()
# Read files
pos = pd.read_csv('output/pos_automotive.csv')
neg = pd.read_csv('output/neg_automotive.csv')

# For this task we only need their reviewText column
pos = pos.reviewText
neg = neg.reviewText

tfidf = TfIdf()
tfidf.add_document(pos, 'p')
tfidf.add_document(neg, 'n')


# print('Printing the frequency of positives')
# print(tfidf.docs[0].nlargest(20, columns=['p_f']))
#
# print('Printing the frequency of negatives')
# print(tfidf.docs[1].nlargest(20, columns=['n_f']))

# Conclusion: frequency does not provide much information on negative result
# We need to check also idf

tfidf.concat_documents()
# tfidf.calculate(scheme=2)
#
# m = tfidf.get_result()
# # print(m)
# pos_r = m.nlargest(1000, columns=['p_tfidf'])[['term', 'p_tfidf']]
# neg_r = m.nlargest(1000, columns=['n_tfidf'])[['term', 'n_tfidf']]
#
# # Plotting
# # plt.figure(0)
# # tfidf.plot(df=pos_r, c='p_tfidf', title='Positive word score', color='blue')
# # plt.figure(1)
# # tfidf.plot(df=neg_r, c='n_tfidf', title='Negative word score', color='red')
# #
# # plt.show()
#
# data = [go.Bar(
#             x=pos_r.p_tfidf,
#             y=pos_r.term,
#             orientation = 'h',
#             name='Positive words',
#     marker=dict(
#         color='rgba(50, 171, 96, 0.6)',
#         line=dict(
#             color='rgba(50, 171, 96, 1.0)',
#             width=1),
#     )
#     )]
#
# plot(data, filename='pos_bar')
#
# data = [go.Bar(
#             x=neg_r.n_tfidf,
#             y=neg_r.term,
#             orientation = 'h',
#             name='Positive words'
#     )]
#
# plot(data, filename='neg_bar')

def scheme_plotter(tfidf, scheme):
    tfidf.calculate(scheme)
    m = tfidf.get_result()
    pos_r = m.nlargest(1000, columns=['p_tfidf'])[['term', 'p_tfidf']]
    neg_r = m.nlargest(1000, columns=['n_tfidf'])[['term', 'n_tfidf']]
    data = [go.Bar(
        x=pos_r.p_tfidf,
        y=pos_r.term,
        orientation='h',
        name='Positive words - Scheme:'+str(scheme),
        marker=dict(
            color='rgba(50, 171, 96, 0.6)',
            line=dict(
                color='rgba(50, 171, 96, 1.0)',
                width=1),
        )
    )]

    plot(data, filename='pos_bar'+str(scheme))

    data = [go.Bar(
        x=neg_r.n_tfidf,
        y=neg_r.term,
        orientation='h',
        name='Negative words - Scheme:' + str(scheme),
    )]

    plot(data, filename='neg_bar'+str(scheme))


scheme_plotter(tfidf, 2)
print(datetime.now() - startTime)
scheme_plotter(tfidf, 3)
scheme_plotter(tfidf, 1)
