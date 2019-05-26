import aiml
import os
import sys
from pkg import helper, cmds
from blessings import Terminal
import time, webbrowser, datetime
import requests

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

class LittleBrain():
  def __init__(self):
    self.t = Terminal()
    self.kernel = aiml.Kernel()
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
          print(self.t.blue(bot_response).lower().strip())


if __name__ == '__main__':
  wiki = WikiApi()



  lb = LittleBrain()
  lb.talk()