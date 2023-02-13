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
from tensorflow.keras.layers import Dense, Activation, concatenate
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Embedding, Flatten

from sklearn.model_selection import train_test_split
import glob
import json

import os

import tensorflow as tf
from keras.models import Model, load_model


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
    

df_review.to_csv('review_data.csv')
    
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




X_gr = data.iloc[:, 7]

tfdf = tfidf.fit_transform(X_gr)


X_gr = tfdf.todense()


Y_gr = data.iloc[:, 11]

X_train, X_test, y_train, y_test = train_test_split(X_gr, Y_gr, test_size=0.3, random_state= 20)

model_gr_input = tf.keras.Input(shape=(500,))

model_gr_layer_1 = tf.keras.layers.Dense(500, activation='relu')(model_gr_input)

model_gr_layer_2 = tf.keras.layers.Dense(400, activation='relu')(model_gr_layer_1)

model_gr_layer_3 = tf.keras.layers.Dense(250, activation='relu')(model_gr_layer_2)

model_gr_layer_4 = tf.keras.layers.Dense(200, activation='relu')(model_gr_layer_3)

model_gr_layer_5 = tf.keras.layers.Dense(50, activation='relu')(model_gr_layer_4)

model_gr_layer_6 = tf.keras.layers.Dense(100, activation='relu')(model_gr_layer_5)

model_gr_layer_7 = tf.keras.layers.Dense(20, activation='relu')(model_gr_layer_6)

model_gr_layer_8 = tf.keras.layers.Dense(10, activation='relu')(model_gr_layer_7)


model_gr_layer_9 = tf.keras.layers.Dense(5, activation='relu')(model_gr_layer_8)

output = tf.keras.layers.Dense(1, activation='sigmoid')(model_gr_layer_9)

model_gr = Model(inputs=model_gr_input, outputs=output)

model_gr.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


model_gr.fit(X_train, y_train, epochs=100)

ttest = model_gr.predict(X_test)


smp = "worst service, had a very bad experience"

smp = remove_noise(smp)

smp = tfidf.transform([smp]).todense()

print(model.predict(smp))


df_movie = pd.read_csv('IMDB_Dataset.csv')

df_movie['sentiment'] = label_encoder.fit_transform(df_movie['sentiment'])

df_movie['review'] = df_movie['review'].apply(remove_noise)

df_movie.to_csv('movie_review_lematized.csv', sep='\t')


X = tfidf.fit_transform(df_movie['review']).todense()

Y = df_movie['sentiment']


X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state= 20)




model_movie_input = tf.keras.Input(shape=(500,))

model_movie_layer_1 = tf.keras.layers.Dense(500, activation='relu')(model_movie_input)

model_movie_layer_2 = tf.keras.layers.Dense(400, activation='relu')(model_movie_layer_1)

model_movie_layer_3 = tf.keras.layers.Dense(250, activation='relu')(model_movie_layer_2)

model_movie_layer_4 = tf.keras.layers.Dense(200, activation='relu')(model_movie_layer_3)

model_movie_layer_5 = tf.keras.layers.Dense(50, activation='relu')(model_movie_layer_4)

model_movie_layer_6 = tf.keras.layers.Dense(100, activation='relu')(model_movie_layer_5)

model_movie_layer_7 = tf.keras.layers.Dense(20, activation='relu')(model_movie_layer_6)

model_movie_layer_8 = tf.keras.layers.Dense(10, activation='relu')(model_movie_layer_7)


model_movie_layer_9 = tf.keras.layers.Dense(5, activation='relu')(model_movie_layer_8)

output = tf.keras.layers.Dense(1, activation='sigmoid')(model_movie_layer_9)

model = Model(inputs=model_movie_input, outputs=output)

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


model.fit(X_train, y_train, epochs=100)

ttest = model.predict(X_test)



model_gr.save('gr_review_model.h5')

model.save('movie_review_model.h5')


ld = load_model('gr_review_model.h5')

smp = "worst service, had a very bad experience"

smp = remove_noise(smp)

smp = tfidf.transform([smp]).todense()

print(ld.predict(smp))




import pickle

pickle.dump(tfidf, open("tfidf.pickle", "wb"))

