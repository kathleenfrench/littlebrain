import os, webbrowser
import sys
from pkg import helper, mta
import requests

def Commands(message):
  try:
    if message[0] == "!help":
      helper.Features()
    elif message[0] == "!weather":
      weather = os.popen("curl -s https://wttr.in?0").read()
      print(weather)
    elif message[0] == "!forecast":
      forecast = os.popen("curl -s https://wttr.in").read()
      print(forecast)
    elif message[0] == "!whereis":
      location = ' '.join(message[1:])
      print("let me show you where {} is...".format(location))
      webbrowser.open("https://www.google.co.in/maps?q={0}".format(location))
    elif message[0] == "!mta":
      ## train line single char input, for ex: l
      ## train_station more colloqual, TODO: to standardize/clean inputs, right now
      ## only lorimer, l8th work
      train_line = message[1].lower()
      train_station = message[2].lower()
      mta.MTA().get_next_arrival_time(train_line, train_station)
    elif message[0] == "!todo":
      pass
    elif message[0] == "!jira":
      pass
    elif message[0] == "!movierec":
      pass
    elif message[0] == "!bored":
      pass
    elif message[0] == "!news":
      pass
    elif message[0] == "!pw":
      pass
    elif message[0] == "!links":
      pass
  except:
    print("try using the !help command, i'm not following what you want me to do...")