import aiml
import os
import sys
from pkg import helper, cmds
from blessings import Terminal

LB_FACTS = {
  "name": "little brain",
  "birthday": "yesterday, two seconds ago, tomorrow...really who's to say?",
  "location": "all over the place tbh",
  "gender": "depends on my mood",
  "age": "age ain't nothin but a number bb",
  "party": "all night long",
  "size": "extremely tall"
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
        if message == "quit" or message == "exit" or message == "bye" or message == "gtg": # exit from chat
            print(self.t.blue("k bye..."))
            exit()
        elif message == "save":
            self.kernel.saveBrain("bot_brain.brn")
        # if the message is a command
        elif message == "help":
            helper.Features()
        elif message[:1] == "!":
            split_message = message.split()
            cmds.Commands(split_message)
        else:
            bot_response = self.kernel.respond(message)
            print(self.t.blue(bot_response).lower().strip())


if __name__ == '__main__':
  lb = LittleBrain()
  lb.talk()