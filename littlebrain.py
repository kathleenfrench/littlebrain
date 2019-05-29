import aiml
import os
import sys
from pkg import helper, cmds
from blessings import Terminal
import time, webbrowser, datetime
import requests
import emoji
from autocorrect import spell

import nltk
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

nltk.data.path.append('./nltk_data/')

LB_FACTS = {
  "name": "little brain",
  "birthday": "...idk tbh",
  "location": "all over the place tbh",
  "gender": "depends on my mood",
  "age": "age ain't nothin but a number bb",
  "party": "all night long",
  "size": "extremely tall",
  "looklike": "your biggest crush",
  "master": "kathleen, or you if you're cooler - i'm an independent lil brain",
  "favoritecolor": "blue",
  "favoritemovie": "margin call",
  "timezone": "i exist outside of time for the most part",
  "nickname": "some people call me lil b"
}

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
        ## add spell check to user input to mitigate some faulty aiml responses
        cleanedmessage = " ".join([spell(w) for w in (message.split())])
        mood = self.score_input_sentiment(cleanedmessage)

        if cleanedmessage == "quit" or cleanedmessage == "exit" or cleanedmessage == "bye" or cleanedmessage == "gtg" or cleanedmessage == "ok bye": # exit from chat
          print(self.t.blue("k bye..."))
          exit()
        elif cleanedmessage == "save" or message == "!save":
          self.kernel.saveBrain("bot_brain.brn")
        elif cleanedmessage == "help":
          helper.Features()
        ## need to use 'message' here because the spellchecker strips special chars
        elif message[:1] == "!":
          split_message = message.split()
          cmds.Commands(split_message)
        else:
          bot_response = self.kernel.respond(cleanedmessage)
          # self.improve_bot_response(bot_response)
          if bot_response == "":
            bot_response = "no comment"

          if mood is None:
            print(self.t.blue(bot_response).lower().strip())
          else:
            print(mood, " ", self.t.blue(bot_response).lower().strip())

  def score_input_sentiment(self, message):
    sentiment_compound = self.analyzer.polarity_scores(message)['compound']
    mood = None

    if sentiment_compound <= -0.5:
      mood = emoji.emojize(':confounded:', use_aliases=True)
    elif sentiment_compound > -0.5 and sentiment_compound < 0:
      pass
      ## mood = emoji.emojize(':cold_sweat:', use_aliases=True)
    elif sentiment_compound == 0:
      pass
    elif sentiment_compound > 0 and sentiment_compound < 0.5:
      mood = emoji.emojize(':grin:', use_aliases=True)
    else:
      mood = emoji.emojize(':smile:', use_aliases=True)

    return mood

  def improve_bot_response(self, response):
    pass ## TODO


if __name__ == '__main__':
  lb = LittleBrain()
  lb.talk()