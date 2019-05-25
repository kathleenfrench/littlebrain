def Features(start="\033[1m", mid="\033[93m", end="\033[0;0m", arrow=" --> "):
  print("-------------------- little brain help desk --------------------")
  print("")

  features_dict = {
    "!save": "save the current state of your littlebrain",
    "!whereis <PLACE>": "have littlebrain redirect you to google maps",
    "!weather": "littlebrain fetches the current weather",
    "!forecast": "littlebrain fetches the 3 day forecast",
    "!mta": "see how f'd the subways are, add a specific train (e.g. !mta L) to narrow it down"
  }

  for feature in features_dict.keys():
    print("{}{}{}{}{}{}".format(start, mid, feature, arrow, end, features_dict[feature]))
