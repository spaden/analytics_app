from flask import Flask, request, jsonify


import re
reg = re.compile(r'[a-zA-Z]')

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import random

from keras.models import load_model

import pickle
import pandas as pd
import numpy as np

from sklearn import preprocessing

from datetime import datetime, timedelta

stemming = PorterStemmer()
stop_list = set(stopwords.words('english'))
app = Flask(__name__)

gr_model = load_model('gr_review_model.h5')

movie_model = load_model('movie_review_model.h5')


tfidf = pickle.load(open('tfidf.pickle', 'rb'))

label_encoder = preprocessing.LabelEncoder()


def remove_noise(quote_word):
   words = word_tokenize(quote_word)
   currentQuote = []
   for word in words:
      if word not in stop_list and word.isalpha() and word not in [",", ".", "!", " ", ";"] and reg.match(word):
         currentQuote.append(stemming.stem(word.lower()))

   return " ".join(currentQuote)


def getPredictions(data):
    
    text = remove_noise(data)

    smp = tfidf.transform([text]).todense()

    return round((gr_model.predict(smp)[0][0] + movie_model.predict(smp)[0][0])/2, 5)


def getWordCloud(df, col):
   text = ''

   for wd in df[col]:
      text += ' ' + wd

   return text


def ratingCount(df, col):

   res = {}

   for i in range(5):
      res[i] = df[df[col] == i].count()

   return res


def rating_over_years(df, rating_col, year_col):

   rvRating = df.groupby('year')['rating'].mean().reset_index().sort_values('year', ascending=False)

   ctRating = df.groupby('year')['rating'].count().reset_index().sort_values('year', ascending=False)

   return rvRating, ctRating


def rating_diff_over_years(df, rating_col=0, year_col=0):

   #To be done

   df_data = df.groupby('year')['rating'].rolling(window=2).apply(lambda x: (x.iloc[1] - x.iloc[0])/x.iloc[0])

   df_data.fillna(0, inplace=True)

   print(df_data)





def returnDate(days):
   return datetime.now() - timedelta(days=days)


def returnFormattedDate(days):
   return (datetime.now() - timedelta(days=days)).strftime('%m-%d-%Y')


def generateDates(df):
   for index, row in df.iterrows():
      st = df.iloc[index, 6].split(' ')
      if st[1] == 'months':
         df.iloc[index, 8] = returnDate(int(st[0]) * 30)
         df.iloc[index, 9] = returnFormattedDate(int(st[0]) * 30)
      elif st[1] == 'month':
         df.iloc[index, 8] = returnDate(30)
         df.iloc[index, 9] = returnFormattedDate(30)
      elif st[1] == 'week':
         df.iloc[index, 8] = returnDate(7)
         df.iloc[index, 9] = returnFormattedDate(7)
      elif st[1] == 'weeks':
         df.iloc[index, 8] = returnDate(int(st[0]) * 7)
         df.iloc[index, 9] = returnFormattedDate(int(st[0]) * 7)
      elif st[1] == 'year':
         df.iloc[index, 8] = returnDate(365)
         df.iloc[index, 9] = returnFormattedDate(365)
      elif st[1] == 'years':
         df.iloc[index, 8] = returnDate(int(st[0]) * 365)
         df.iloc[index, 9] = returnFormattedDate(int(st[0]) * 365)
      elif st[1] == 'days':
         df.iloc[index, 8] = returnDate(int(st[0]))
         df.iloc[index, 9] = returnFormattedDate(int(st[0]))
      elif st[1] == 'day':
         df.iloc[index, 8] = returnDate(1)
         df.iloc[index, 9] = returnFormattedDate(1)
   return df

def get_allsentiments():
    df = pd.read_csv('review_data.csv')

    df = generateDates(df)

    df['reviewDate2'] = pd.to_datetime(df['reviewDate2'])

    df['formatted_date'] = pd.to_datetime(df['formatted_date'])

    df['year'] = df['formatted_date'].dt.year

    df['year'] = pd.to_numeric(df['year'])

    # df['lem_sentiment'] = df['reviewText'].apply(remove_noise)
    #
    # df['predsentiment'] = df['lem_sentiment'].apply(getPredictions)

    #rating_diff_over_years(df)
    
    #print(df['predsentiment'])
    


@app.route("/getsentiment", methods=['POST'])
def postTest():
   global gr_model, movie_model, tfidf
    
   data = request.json

   text = remove_noise(data['userinput'])


   smp = tfidf.transform([text]).todense()
   
   get_allsentiments()

   return {
      'result': 'ok' #[str(gr_model.predict(smp)[0][0]), str(movie_model.predict(smp)[0][0])]
   }



if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port = '8002')