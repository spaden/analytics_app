from flask import Flask, request, jsonify

import remove_noise
import dateutilmod


from keras.models import load_model

import pickle
import pandas as pd
import numpy as np

from sklearn import preprocessing

import pingouin as pg


app = Flask(__name__)

gr_model = load_model('../gr_review_model.h5')

movie_model = load_model('../movie_review_model.h5')


tfidf = pickle.load(open('../tfidf.pickle', 'rb'))

label_encoder = preprocessing.LabelEncoder()





def getPredictions(data):
    
    text = remove_noise.remove_noise(data)

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

   df_data = df.groupby('year')['rating'].mean().rolling(window=2).apply(lambda x: (x.iloc[1] - x.iloc[0])/x.iloc[0]).fillna(0)

   return df_data


def calculate_clt(data):
   tt = []
   for i in range(100000):
      tt.append(np.mean(data.sample(50, replace=True)))
   ci = np.percentile(tt, [2.5, 97.5])
   return ci


def ptest(df):
   year_ttest = pg.pairwise_ttests(data=df, dv='rating', between=['year'])

   return year_ttest


def get_allsentiments():
    df = pd.read_csv('../review_data.csv')

    df = dateutilmod.generateDates(df)

    df['reviewDate2'] = pd.to_datetime(df['reviewDate2'])

    df['formatted_date'] = pd.to_datetime(df['formatted_date'])

    df['year'] = df['formatted_date'].dt.year

    df['year'] = pd.to_numeric(df['year'])

    # df['lem_sentiment'] = df['reviewText'].apply(remove_noise)
    #
    # df['predsentiment'] = df['lem_sentiment'].apply(getPredictions)

    rating_diff_over_years(df)
    
    #print(df['predsentiment'])
    


@app.route("/getsentiment", methods=['POST'])
def postTest():
   global gr_model, movie_model, tfidf
    
   data = request.json

   text = remove_noise.remove_noise(data['userinput'])


   smp = tfidf.transform([text]).todense()
   
   get_allsentiments()

   return {
      'result': 'ok' #[str(gr_model.predict(smp)[0][0]), str(movie_model.predict(smp)[0][0])]
   }



if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port = '8002')