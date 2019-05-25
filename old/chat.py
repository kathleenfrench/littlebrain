import io
import random
import string
import warnings
import sys
import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np 

import nltk
from nltk.stem import WordNetLemmatizer

warnings.filterwarnings('ignore')

#3 nltk.download('popular', quiet=True)

## nltk.download('punkt') # first run only
## nltk.download('wordnet') # first run only

with open('cleaned-scotus.txt', 'r', encoding='utf8', errors='ignore') as fin:
  raw = fin.read()


print('raw value set')

sent_tokens = nltk.sent_tokenize(raw) # converts to list of sentences
word_tokens = nltk.word_tokenize(raw) # converts to list of words

print('sent and word tokens generated...')

sent_tokens[:2]
word_tokens[:5]

lemmer = WordNetLemmatizer()

def LemTokens(tokens):
  return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
  return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

INTRO_INPUTS = ("good morning", "hello", "greetings", "we will now hear arguments")
INTRO_RESPONSES = ("good morning", "may it please the court", "thank you", "your honor")

## check for intro
def intro(sentence):
  for word in sentence.split():
    if word.lower() in INTRO_INPUTS:
      return random.choice(INTRO_RESPONSES)

def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"You are out of line, counselor"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

flag=True
print("SCOTUS: Welcome to the Supreme Court of the United States. We will now hear arguments on the case before us. If you wish to leave, type 'request for recess'")

while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='request for recess'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("SCOTUS: We will readjourn in an hour")
        else:
            if(intro(user_response)!=None):
                print("SCOTUS: "+intro(user_response))
            else:
                print("SCOTUS: ",end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("SCOTUS: Court is adjourned")