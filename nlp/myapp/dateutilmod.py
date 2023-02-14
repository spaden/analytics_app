import pandas as pd
import numpy as np

from datetime import datetime, timedelta

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