## https://github.com/neoterix/nyc-mta-arrival-notify/blob/master/mta_notification.py

import os, webbrowser
import time # imports module for Epoch/GMT time conversion
import requests
from google.transit import gtfs_realtime_pb2
from dotenv import load_dotenv, find_dotenv
from protobuf_to_dict import protobuf_to_dict

## API KEYS
# load_dotenv(find_dotenv())
# mta_key = os.environ['MTA_KEY']

TRAINS = {
  "l8th": 'L01S',
  "lorimer": 'L10N'
}

## given it's nowhere in the docs, it's worth noting here...
## feed_id=2 for L TRAIN
## feed_id=21 for B/D/F/M
## no feed id needed for 1/2/3/4/5/6
L_FEED_ID = 2
BDFM_FEED_ID = 21

class MTA(object):
  def __init__(self):
    load_dotenv(find_dotenv())
    self.mta_key = os.environ["MTA_KEY"]
  
    ## ENDPOINTS
    self.l_train_endpoint = 'http://datamine.mta.info/mta_esi.php?key={}&feed_id={}'.format(self.mta_key, L_FEED_ID)
    self.bdfm_trains_endpoint = 'http://datamine.mta.info/mta_esi.php?key={}&feed_id={}'.format(self.mta_key, BDFM_FEED_ID)
    self.t123456_trains_endpoint = 'http://datamine.mta.info/mta_esi.php?key={}'.format(self.mta_key)

    ## REALTIME FEED
    self.feed = gtfs_realtime_pb2.FeedMessage()
    self.collected_times = []
    self.realtime_data = list()

  def get_realtime_data(self, train_line):
    if train_line == 'l':
      response = requests.get(self.l_train_endpoint)
    elif train_line == 'b' or train_line == 'd' or train_line == 'f' or train_line == 'm':
      response = requests.get(self.bdfm_trains_endpoint)
    else:
      response = requests.get(self.t123456_trains_endpoint)

    self.feed.ParseFromString(response.content)

    subway_feed = protobuf_to_dict(self.feed)
    self.realtime_data = subway_feed['entity']

# The MTA data feed uses the General Transit Feed Specification (GTFS) which
# is based upon Google's "protocol buffer" data format. While possible to
# manipulate this data natively in python, it is far easier to use the
# "pip install --upgrade gtfs-realtime-bindings" library which can be found on pypi

# subway_feed = protobuf_to_dict(feed) # subway_feed is a dictionary
# realtime_data = subway_feed['entity'] # train_data is a list

# Because the data feed includes multiple arrival times for a given station
# a global list needs to be created to collect the various times
# collected_times = []

  # This function takes a converted MTA data feed and a specific station ID and
  # loops through various nested dictionaries and lists to (1) filter out active
  # trains, (2) search for the given station ID, and (3) append the arrival time
  # of any instance of the station ID to the collected_times list
  def station_time_lookup(self, train_data, station):
      for trains in train_data: # trains are dictionaries
          if trains.get('trip_update', False) != False:
              unique_train_schedule = trains['trip_update'] 
              unique_arrival_times = []

              try:
                # train_schedule is a dictionary with trip and stop_time_update
                unique_arrival_times = unique_train_schedule['stop_time_update']
              except KeyError:
                pass

              # arrival_times is a list of arrivals
              # arrivals are dictionaries with time data and stop_ids
              for scheduled_arrivals in unique_arrival_times:
                  # stop_id = scheduled_arrivals.get('stop_id').replace("")
                  if scheduled_arrivals.get('stop_id') == station:
                      time_data = []
                      unique_time = []

                      try:
                        time_data = scheduled_arrivals['arrival']
                        unique_time = time_data['time']

                        if unique_time != None:
                            self.collected_times.append(unique_time)
                      except KeyError:
                        pass

  def get_next_arrival_time(self, train_line, station):
    self.get_realtime_data(train_line)

    # Run the above function for the station ID 
    self.station_time_lookup(self.realtime_data, TRAINS[station])

    # Sort the collected times list in chronological order (the times from the data
    # feed are in Epoch time format)
    self.collected_times.sort()

    # Pop off the earliest and second earliest arrival times from the list
    nearest_arrival_time = self.collected_times[0]
    second_arrival_time = self.collected_times[1]

    # Grab the current time so that you can find out the minutes to arrival
    current_time = int(time.time())
    time_until_train = int(((nearest_arrival_time - current_time) / 60))

    # This final part of the code checks the time to arrival and prints a few
    # different messages depending on the circumstance
    if time_until_train > 3:
        print(f"""
    it's currently {time.strftime("%I:%M %p")}
    the next Brooklyn-bound {train_line} train from
    {station} arrives in
    {time_until_train} minutes at {time.strftime("%I:%M %p", time.localtime(nearest_arrival_time))}""")
        print("")
    elif time_until_train <= 0:
        print(f"""
    welp... You *just* missed the train. (╯°□°）╯︵ ┻━┻
    Ah well, the next train will arrive at {time.strftime("%I:%M %p", time.localtime(second_arrival_time))}""")
        print("")
    else:
      print(f"""
    HURRY UP YOU HAVE {time_until_train} MINUTES TO GET TO
    {station.upper()} IF YOU WANT TO GET HOME!
    THE TRAIN GETS IN AT {time.strftime("%I:%M %p", time.localtime(nearest_arrival_time))}""")
      print("")