#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file includes pre-defined classes and functions used in the machine learning project.
"""

import os

# data manipulation and data clean
import numpy as np
from collections import Counter
from scipy.sparse import csr_matrix

# scikit-learn
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import classification_report, confusion_matrix, f1_score, \
                            precision_score, recall_score
from sklearn.feature_extraction.text import TfidfTransformer


# self-defined module
from document import document



## ***************** data extraction *************************
def parse_files(path):
    '''Parse document file pathes and labels from data path
    Parameters
    ----------
    path : str
        Source data file path
    Return
    ------
    file_path_list : list
        List of file paths of all documents
    ylabel: list
        List of classes each document belongs to
    '''

    folders = [f for f in os.listdir(path) if not f.startswith('.')]
    file_path_list = [] # list of file paths of all documents
    ylabel = []# list of classes each document belongs to

    for folder in folders:
        folder_path = os.path.join(path, folder)
        file_path = [os.path.join(folder_path,f) for f in os.listdir(folder_path)\
                     if not f.startswith('.')]
        file_path_list.extend(file_path)
        ylabel.extend([folder]*len(file_path))

    # TODO: remove incompatible files

    return file_path_list, ylabel

def load_document(path, label, header_seperator='\n\n'):
    ''' Load document from file path, return document class'''

    with open(path, 'r') as file:
        return document(path,label).parser(file,header_seperator)


## ***************** data preprocessing *************************
def clean_document(document_data, **kwargs):
    ''' Call `clean_text` method for a single document object,
    overwrite the object directly, return nothing
    '''
    document_data.clean_text(**kwargs)

def clean_all_documents(documents_data, **kwargs):
    ''' Call `clean_text` method for every single document object included in the list
    parameter is a list of document objects, overwrite the object directly, return nothing
    '''
    for i, doc in enumerate(documents_data):
        documents_data[i].clean_text(**kwargs)

def label_encoder(train, test=None, encoder='ordinal'):
    # ordinal encoding
    if encoder == 'ordinal':
        ordinal_encoder = OrdinalEncoder()
        y_train= ordinal_encoder.fit_transform(np.array(train).reshape(-1, 1)).reshape(1,-1)[0]
        if test:
            y_test = ordinal_encoder.transform(np.array(test).reshape(-1, 1)).reshape(1,-1)[0]
        category = ordinal_encoder.categories_[0].tolist()

    # one-hot encoding
    elif encoder == 'onehot':
        onehot_encoder = OneHotEncoder(sparse=False)
        y_train = onehot_encoder.fit_transform(np.array(train).reshape(-1, 1))
        if test:
            y_test = onehot_encoder.transform(np.array(test).reshape(-1, 1))
        category = onehot_encoder.categories_[0].tolist()
    else:
        raise ValueError('encoder should be `ordinal` or `onehot`')

    if test:
        return y_train, y_test, category
    else:
        return y_train, category

## ********************* bag of word ***************************
class DocumentSelector(BaseEstimator, TransformerMixin):
    '''Class to select a list of attributes from a list document objects'''

    def __init__(self, attribute_names):
        self.attribute_names = attribute_names

    def fit(self, X, y = None):
        return self

    def transform(self, X, y = None):
        return [x.get(self.attribute_names) for x in X]


class DocumentToWordCounterTransformer(BaseEstimator, TransformerMixin):
    '''Class to convert a list of text to word count array'''

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X_transformed = []
        for text in X:
            word_counts = Counter(text.split())
            X_transformed.append(word_counts)
        return np.array(X_transformed)


class WordCounterToVectorTransformer():
    '''Class to convert count array to sparse matrix containing word count vector'''

    def __init__(self, vocabulary_size=10000):
        self.vocabulary_size = vocabulary_size

    def fit(self, X, y=None):
        total_count = Counter()
        for word_count in X:
            for word, count in word_count.items():
                total_count[word] += min(count, 10)
        most_common = total_count.most_common(self.vocabulary_size)
        self.most_common_ = most_common
        self.vocabulary_ = {word: index + 1 for index, (word, count) in enumerate(most_common)}
        return self

    def transform(self, X, y=None):
        rows = []
        cols = []
        data = []
        for row, word_count in enumerate(X):
            for word, count in word_count.items():
                rows.append(row)
                cols.append(self.vocabulary_.get(word, 0))
                data.append(count)
        return csr_matrix((data, (rows, cols)), shape=(len(X), self.vocabulary_size + 1))


BagOfWord = Pipeline([
        ('select_text', DocumentSelector(['body'])),
        ('document_to_wordcount', DocumentToWordCounterTransformer()),
        ('wordcount_to_vector', WordCounterToVectorTransformer(vocabulary_size=5000)),
        # TODO: normalize by len_of_body?
])

#FeatureAugmentation = Pipeline([
#        ('select_num', DocumentSelector(['num_of_words','num_of_special_char','num_of_numbers'])),
#        ('std_scalar',StandardScaler()),
#])

Tfidf = Pipeline([
        ('select_text', DocumentSelector(['body'])),
        ('document_to_wordcount', DocumentToWordCounterTransformer()),
        ('wordcount_to_vector', WordCounterToVectorTransformer(vocabulary_size=5000)),
        ('tfidf', TfidfTransformer()),
        ])

""" Support Vector Machine (SVM) classifier"""
svm_clf = Pipeline([
        ('select_text', DocumentSelector(['body'])),
        ('document_to_wordcount', DocumentToWordCounterTransformer()),
        ('wordcount_to_vector', WordCounterToVectorTransformer(vocabulary_size=5000)),
        ('tfidf', TfidfTransformer()),
        ('clf', SGDClassifier(penalty='l2', alpha=5e-5, random_state=42)),
])
