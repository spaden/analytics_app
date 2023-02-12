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
import glob
import json

import os

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
#embedding_layer = Embedding(input_dim=50,output_dim=100,input_length=500)
#model.add(embedding_layer)
#model.add(Flatten())



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


filenames = next(os.walk('./formatted_data'))[2]

df_review = pd.DataFrame()

def createDataFrame(file):
    global df_review
    with open('./formatted_data/'+file, 'r') as f:
        data = json.loads(f.read())
        tt = pd.json_normalize(data)
        
        if 'all_reviews' in tt.keys():
            tt = pd.json_normalize(tt['all_reviews'])
            print(tt)
            
        else:
        
            tt['userType'].fillna('Not defined', inplace=True)
        
            tt['prevReviewCount'].fillna(0, inplace=True)
        
            tt['prevPhotosReview'].fillna(0, inplace=True)
            
            tt['reviewDate2'] = None
            tt['formatted_date'] = None
            tt['location'] = file.split('.')[0]
            
            df_review = pd.concat([df_review, tt], ignore_index=True)
    

for file in filenames:
    createDataFrame(file)
    
    
complaints = df_review[df_review['rating'] <= 3]

compliments = df_review[(df_review['rating'] >=4) & (df_review['rating'] <=5)]


compliments['reviewText'] = compliments['reviewText'].apply(remove_noise)
complaints['reviewText'] = complaints['reviewText'].apply(remove_noise)

Y = []

for i in range(len(compliments)):
    Y.append(1)
    
for i in range(len(complaints)):
    Y.append(0)
    
Y = pd.DataFrame(Y)

data = pd.concat([compliments, complaints], ignore_index = True)

data = pd.concat([data, Y], axis=1, ignore_index=True)

data = data.sample(frac=1).reset_index(drop=True)




X = data.iloc[:, 7]

tfdf = tfidf.fit_transform(X)


X = tfdf.todense()


Y = data.iloc[:, 11]

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state= 20)

model = Sequential()

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


model.fit(X_train, y_train, epochs=100)

ttest = model.predict(X_test)


smp = "worst service, had a very bad experience"

smp = remove_noise(smp)

smp = tfidf.transform([smp]).todense()

print(model.predict(smp))



