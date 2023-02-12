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

stemming = PorterStemmer()
stop_list = set(stopwords.words('english'))
app = Flask(__name__)


def remove_noise(quote_word):
   words = word_tokenize(quote_word)
   currentQuote = []
   for word in words:
      if word not in stop_list and word.isalpha() and word not in [",", ".", "!", " ", ";"] and reg.match(word):
         currentQuote.append(stemming.stem(word.lower()))

   return " ".join(currentQuote)



@app.route("/getsentiment", methods=['POST'])
def postTest():
   data = request.json

   text = remove_noise(data['userinput'])


   gr_model = load_model('gr_review_model.h5')

   movie_model = load_model('movie_review_model.h5')


   tfidf = pickle.load(open('tfidf.pickle', 'rb'))

   smp = tfidf.transform([text]).todense()



   return {
      'result': [str(gr_model.predict(smp)[0][0]), str(movie_model.predict(smp)[0][0])]
   }

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port = '8002')