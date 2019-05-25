import os
import sys
# sys.path.append("pkg/")
# import helper
from pkg import helper

def Commands(message):
  try:
    if message[0] == "!help":
      helper.Features()
  except:
    print("try using the !help command, i'm not following...")