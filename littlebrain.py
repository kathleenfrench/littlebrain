import aiml
import os
import sys
from pkg import helper, cmds
from blessings import Terminal
import time, webbrowser, datetime
import requests
import emoji

import nltk
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


nltk.data.path.append('./nltk_data/')

## info
from wikiapi import WikiApi

LB_FACTS = {
  "name": "little brain",
  "birthday": "...idk tbh",
  "location": "all over the place tbh",
  "gender": "depends on my mood",
  "age": "age ain't nothin but a number bb",
  "party": "all night long",
  "size": "extremely tall",
  "looklike": "your biggest crush",
  "master": "kathleen, or you if you're cooler"
}

## sentiment scores
MAX_NEGATIVE = "xxx"
NEGATIVE = "xxy"
NEUTRAL = "xyx"
POSITIVE = "xyy"
MAX_POSITIVE = "yxx"

class LittleBrain():
  def __init__(self):
    self.t = Terminal()
    self.kernel = aiml.Kernel()
    self.analyzer = SentimentIntensityAnalyzer()
    if os.path.isfile("bot_brain.brn"):
      self.kernel.bootstrap(brainFile="bot_brain.brn")
    else:
      self.kernel.bootstrap(learnFiles=os.path.abspath("aiml/std-startup.xml"), commands="load aiml b")
      self.kernel.saveBrain("bot_brain.brn")

    for key, val in LB_FACTS.items():
      self.kernel.setBotPredicate(key, val)

  def talk(self):
    ## clears the terminal
    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        message = input(">> ")
        split_message = message.split()

        sentiment_score, mood = self.score_input_sentiment(message)

        if message == "quit" or message == "exit" or message == "bye" or message == "gtg" or message == "ok bye": # exit from chat
          print(self.t.blue("k bye..."))
          exit()
        elif message == "save" or message == "!save":
          self.kernel.saveBrain("bot_brain.brn")
        # if the message is a command
        elif message == "help":
          helper.Features()
        # elif "where is" in message:
        #   location = split_message[2]
        #   print("let me show you where {} is...".format(location))
        #   webbrowser.open("https://www.google.co.in/maps?q={0}".format(location))
        elif "what's today" in message:
          today = "today is {0}".format(datetime.datetime.utcnow().date().strftime('%Y-%m-%d'))
          print(today)
        elif message[:1] == "!":
          cmds.Commands(split_message)
        else:
          bot_response = self.kernel.respond(message)
          # self.improve_bot_response(bot_response)

          if mood is None:
            print(self.t.blue(bot_response).lower().strip())
          else:
            print(mood, " ", self.t.blue(bot_response).lower().strip())

  def score_input_sentiment(self, message):
    sentiment_compound = self.analyzer.polarity_scores(message)['compound']
    score = None
    mood = None

    if sentiment_compound <= -0.5:
      score = MAX_NEGATIVE
      mood = emoji.emojize(':confounded:', use_aliases=True)
    elif sentiment_compound > -0.5 and sentiment_compound < 0:
      score = NEGATIVE
      mood = emoji.emojize(':cold_sweat:', use_aliases=True)
    elif sentiment_compound == 0:
      score = NEUTRAL
    elif sentiment_compound > 0 and sentiment_compound < 0.5:
      score = POSITIVE
      mood = emoji.emojize(':grin:', use_aliases=True)
    else:
      score = MAX_POSITIVE
      mood = emoji.emojize(':smile:', use_aliases=True)

    return score, mood

  def improve_bot_response(self, response):
    dict = {}
    sentence = response.lower().strip()
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentence)
    parsed_input = [wt for wt in word_tokens if not wt in stop_words]
    tagged = nltk.pos_tag(parsed_input)
    new_response = ""

    for word in tagged:
      try:
        wtype = word[1]
        if (dict[wtype] != None):
          part_of_speech = dict[wtype]
        else:
          part_of_speech = 'NOUN'
        
        if part_of_speech == 'NOUN':
          word_mod = wordnet.morphy(word[0], wordnet.NOUN)
        elif part_of_speech == 'VERB':
          word_mod = wordnet.morphy(word[0], wordnet.VERB)
        elif part_of_speech == 'ADV':
          word_mod = wordnet.morphy(word[0], wordnet.ADV)
        elif part_of_speech == 'ADJ':
          word_mod = wordnet.morphy(word[0], wordnet.ADJ)

        updated_word = wordnet.synsets(word_mod)[0].lemmas()[0].name()

      except:
        updated_word = word[0]

      if new_response == "":
        new_response = new_response + updated_word.lower()
      else:
        new_response = new_response + " " + updated_word.lower()

      print("NEW RESPONSE: ", new_response)


if __name__ == '__main__':
  wiki = WikiApi()



  lb = LittleBrain()
  lb.talk()