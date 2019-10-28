import random
import json
from os import walk
import operator
import re
#import lyricsgenius
filenames = []
for (dirpath, dirnames, filenames_list) in walk("./songs"):
  filenames.extend(filenames_list)
  break

lyrics = []
for filename in filenames:
  try:
    file = open("./songs/"+filename)
    lines = file.readlines()
    json_str = ' '.join(lines)
    loaded_json = json.loads(json_str)
    song_lyrics = loaded_json['songs'][0]['lyrics'].lower()
    #replace all the \n's with " "
    while song_lyrics.find("\n") != -1:
      song_lyrics = song_lyrics.replace("\n", " ")
    lyrics.append(song_lyrics)
    file.close()
  except:
    #print("ERROR: %s not found!" %filename)
    continue
    
wordsData = {} #word, nextWordList
for song_lyrics in lyrics:
  #song_lyrics = re.sub(rePattern, '', song_lyrics)
  words = song_lyrics.split(" ")
  counter = 0
  while counter < len(words) - 1:
    word1, word2 = words[counter], words[counter + 1]
    if len(word1) > 0 and len(word2) > 0:
      if word1[-1] in ".,'!):(?": word1 = word1[:-1]
      if word2[-1] in ".,'!):(?": word2 = word2[:-1]
      if word1 in wordsData.keys():
        wordsData[word1].append(word2)
      else:
        wordsData[word1] = [word2]
    counter += 1


def getAvgLyricsLength():
  lengths = [len(song) for song in lyrics]
  return int(sum(lengths) / len(lyrics))


def getNextWord(currentWord, second=False):
  nextWordsList = wordsData[currentWord]
  #return random.choice(nextWordsList)
  wordsCount = {}#word, word count
  for nextWord in nextWordsList:
    if nextWord in wordsCount:
      wordsCount[nextWord] += 1
    else:
      wordsCount[nextWord] = 0
  #sortedWords = sorted(wordsCount.items(), key=operator.itemgetter(1))
  #return random.choice(sortedWords[-3:])[0]
  '''if second:
    return sortedWords[-2][0]
  return sortedWords[-1][0]'''
  #choose corresponding key of max value
  return max(wordsCount.items(), key=operator.itemgetter(1))[0]

#let the starting word be randomly chosen
currentWord = random.choice(list(wordsData.keys()))

maxWords = getAvgLyricsLength()
prevWords = []
for x in range(maxWords):
  try:
    currentWord = getNextWord(currentWord)
    if len(prevWords) > 5:
      seq = prevWords[x-5:]
      if currentWord in seq:
        currentWord = getNextWord(seq[-1], second=True)
    prevWords.append(currentWord)
    print(currentWord, end=" ")
  except:
    continue