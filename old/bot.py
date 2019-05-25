from flask import Flask, render_template, request
from flask_socketio import SocketIO

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging

import aiml



# app = Flask(__name__)
# socketio = SocketIO(app)

littlebrain = ChatBot(
  'littlebrain',
  storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
  database="littlebrain_db",
  database_uri="mongodb://mongoadmin:secret@mongo:27017/littlebrain_db",
  logic_adapters=[
    'chatterbot.logic.BestMatch'
  ],
)

# trainer for littlebrain
trainer = ChatterBotCorpusTrainer(littlebrain)

# train littlebrain
trainer.train("chatterbot.corpus.english")

# initial response to user input
print("hi, i'm littlebrain!")

# following loop will execute each time the user inputs info
while True:
  try:
    user_input = input()
    littlebrain_response = littlebrain.get_response(user_input)
    print(littlebrain_response)

  # press ctrl-c or ctrl-d to exit
  except(KeyboardInterrupt, EOFError, SystemExit):
    break

# if __name__ == "__main__":
#   app.run()