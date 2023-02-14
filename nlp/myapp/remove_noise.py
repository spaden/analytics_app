from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

stemming = PorterStemmer()
stop_list = set(stopwords.words('english'))

import re
reg = re.compile(r'[a-zA-Z]')

def remove_noise(quote_word):
   words = word_tokenize(quote_word)
   currentQuote = []
   for word in words:
      if word not in stop_list and word.isalpha() and word not in [",", ".", "!", " ", ";"] and reg.match(word):
         currentQuote.append(stemming.stem(word.lower()))

   return " ".join(currentQuote)

