def Features(start="\033[1m", mid="\033[93m", end="\033[0;0m", arrow=" --> "):
  features_dict = {
    "be my friend": "!bff",
    "url scan": "!urlscan <URL-TO-SCAN>"
  }

  for feature in features_dict.keys():
    print("{}{}{}{}{}{}".format(start, mid, feature, arrow, end, features_dict[feature]))
