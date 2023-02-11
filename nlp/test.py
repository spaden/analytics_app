# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 10:09:27 2023

@author: KalyanRuchiPC
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud


from gensim.corpora.dictionary import Dictionary
from nltk.tokenize import word_tokenize

from gensim import similarities
from gensim.models.tfidfmodel import TfidfModel

from sklearn.feature_extraction.text import TfidfVectorizer


from sklearn import preprocessing

label_encoder = preprocessing.LabelEncoder()

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Embedding, Flatten

from sklearn.model_selection import train_test_split


stemming = PorterStemmer()
stop_list = set(stopwords.words('english'))

df = pd.read_csv('text_spam.csv')



df['spam_not'] = label_encoder.fit_transform(df['Category'])

df.drop('Category', axis=1, inplace=True)




import re
reg = re.compile(r'[a-zA-Z]')

def remove_noise(quote_word):
    words = word_tokenize(quote_word)
    currentQuote = []
    for word in words:
        if word not in stop_list and word.isalpha() and word not in [",", ".", "!", " ", ";"] and reg.match(word):
                currentQuote.append(stemming.stem(word.lower()))
    
    return " ".join(currentQuote)


df['Message'] = df['Message'].apply(remove_noise)




def generate_corpus(col):
    global index
    tokenized_docs = [word_tokenize(doc.lower()) for doc in col]
    
    dictionary = Dictionary(tokenized_docs)
    
    corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]
    
    print(corpus)
    
    test = TfidfModel(corpus)
    
    
    index = similarities.SparseMatrixSimilarity(test[corpus], num_features=len(dictionary))
    
    return index.index.todense()



tfidf = TfidfVectorizer(stop_words='english', max_features=500)

X = tfidf.fit_transform(df['Message'])


X = X.todense()

df_new = pd.DataFrame(X)



X_train, X_test, y_train, y_test = train_test_split(df_new, df['spam_not'], test_size=0.3, random_state= 20)



model = Sequential()
embedding_layer = Embedding(input_dim=50,output_dim=100,input_length=500)
model.add(embedding_layer)
model.add(Flatten())



model.add(Dense(500, input_shape=(500,), activation='relu'))

model.add(Dense(100, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(5, activation='relu'))
model.add(Dense(2, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


model.fit(X_train, y_train, epochs=50)

ttest = model.predict(X_test)


mn = 100000


def computedist(a1, a2, b1, b2):
    res = (a2-a1) ** 2 + (b2-b1) ** 2
    
    
    return round(res ** 0.5, 4)


dt = [[0.4, 0.53],
      [0.22, 0.38],
      [0.35, 0.32],
      [0.26, 0.19],
      [0.08, 0.41],
      [0.43, 0.3]]

for i in range(len(dt)):
    mn = 10000
    for j in range(len(dt)):
        
        res = computedist(dt[i][0], dt[j][0], dt[i][1], dt[j][1])

            
        if res < mn and res != 0:
            mn = res
            
    print('Min for P' + str(i) + ' ' + str(mn))
