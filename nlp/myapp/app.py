from flask import Flask, request, jsonify

import remove_noise
import dateutilmod


from keras.models import load_model

import pickle
import pandas as pd
import numpy as np

from sklearn import preprocessing

import pingouin as pg

import json

app = Flask(__name__)

gr_model = load_model('../gr_review_model.h5')

movie_model = load_model('../movie_review_model.h5')


tfidf = pickle.load(open('../tfidf.pickle', 'rb'))

label_encoder = preprocessing.LabelEncoder()





def getPredictions(data):

    text = remove_noise.remove_noise(data)

    smp = tfidf.transform([text]).todense()

    return round((gr_model.predict(smp)[0][0] + movie_model.predict(smp)[0][0])/2, 5)


def getWordCloud(df):
   text = ''

   for wd in df['reviewText']:
      text += ' ' + wd

   return text


def ratingCount(df):

   res = {}

   for i in range(1, 6):
      res[i] = int(df[df['rating'] == i].count()['rating'])

   return json.dumps(res)


def rating_over_years(df):

   rvRating = df.groupby('year')['rating'].mean().reset_index().sort_values('year', ascending=False)

   ctRating = df.groupby('year')['rating'].count().reset_index().sort_values('year', ascending=False)

   return {
      'rating': rvRating.to_json(),
      'ctrating': ctRating.to_json()
   }



def rating_diff_over_years(df):

   df_data = df.groupby('year')['rating'].mean().rolling(window=2).apply(lambda x: (x.iloc[1] - x.iloc[0])/x.iloc[0]).fillna(0)

   return df_data.to_json()


def calculate_clt(data):
   tt = []
   for i in range(10):
      tt.append(np.mean(data.sample(50, replace=True)))
   ci = np.percentile(tt, [2.5, 97.5])

   print(list(ci))
   return ci.tolist()


def ptest(df):
   lst = df['year'].unique()

   res = {}


   for i in range(len(lst)):
      for j in range(len(lst)):

         if i == j:
            continue

         try:

            rest = pg.ttest(df[df['year'] == lst[i]]['rating'],
                            df[df['year'] == lst[j]]['rating'],
                            correction=True)

            if str(rest['p-val']['T-test']) != 'nan':
               res[str(lst[i]) + ' - ' + str(lst[j])] = str(rest['p-val']['T-test'])

         except:
            pass
   return json.dumps(res)



@app.route("/getallsentiments", methods=['GET'])
def get_allsentiments():
    print('entered')
    df = pd.read_csv('../review_data.csv')


    df = df.iloc[:5, :]

    df = dateutilmod.generateDates(df)

    df['reviewDate2'] = pd.to_datetime(df['reviewDate2'])

    df['formatted_date'] = pd.to_datetime(df['formatted_date'])

    df['year'] = df['formatted_date'].dt.year

    df['reviewText'].fillna('No Reivew', inplace=True)

    df['predsentiment'] = df['reviewText'].apply(getPredictions)

    pTestRes = ptest(df)


    cI = calculate_clt(df['rating'])

    ratDiffOverYears = rating_diff_over_years(df)

    ratOverYears = rating_over_years(df)

    ratCount = ratingCount(df)

    worMapPos = getWordCloud(df[df['predsentiment'] >= 0.6])

    wordMapNeg = getWordCloud(df[df['predsentiment'] <= 0.5])


    return {
       'orgSent': df.to_json(orient ='records', force_ascii=False),
       'wordCloud': {
          'positive': worMapPos,
          'negative': wordMapNeg
       },
       'ratingCount': ratCount,
       'ratingOverYears': ratOverYears,
       'ratDifferenceYears': ratDiffOverYears,
       'confidence_interval': cI,
        'ptests': pTestRes
    }


@app.route("/getsentiment", methods=['POST'])
def getSentiment():
   global gr_model, movie_model, tfidf

   data = request.json

   text = remove_noise.remove_noise(data['userinput'])


   smp = tfidf.transform([text]).todense()

   return {
      'result': [str(gr_model.predict(smp)[0][0]), str(movie_model.predict(smp)[0][0])]
   }


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port = '8004', threaded=True)