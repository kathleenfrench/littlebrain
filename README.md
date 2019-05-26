# LITTLE BRAIN

### WHAT (OR WHO) IS LITTLE BRAIN?

little brain is a CLI tool/personal assistant/friend written in python

### INSTALL
```
make install
```

### RUN
```
make small_talk
```
- say whatever you want to little brain, the more you talk the more you can teach him
- to save your progress and help grow his brain say `!save`
- to leave, just tell him `bye`

### BUILT-IN FEATURES
```
!save --> save the current state of your littlebrain
!whereis <PLACE> --> have littlebrain redirect you to google maps
!weather --> littlebrain fetches the current weather
!forecast --> littlebrain fetches the 3 day forecast
!mta --> see how f'd the subways are, add a specific train + station (current support for [!mta L lorimer | !mta L 8th | !mta L union]) to narrow it down
!l <LINK> --> link shortcuts, can either input as a full https://link.com or link w/o protocol/.com
```

#### MTA FEATURE

- create an `.env` file in `/pkg` 
- put `MTA_KEY=(your api key)`
- you can register for one [HERE](http://datamine.mta.info/feed-documentation)

#### WIKIPEDIA_FEATURE

- because of a bug in the python wikipedia wrapper, a modification needs to be made on line `389` of the `wikipedia.py` package to provide a parser:

```
lis = BeautifulSoup(html, 'html.parser').find_all('li')
```