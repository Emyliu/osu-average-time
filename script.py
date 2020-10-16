import requests
import json
import unidecode
import re

# This script uses the Osu API V1 because the V2 OAuth endpoint is busted...

# Config 
SECRET_KEY = "???"
USERNAME = "???"
NUMBER_OF_PLAYS = 50

payload = {
"k": SECRET_KEY,
"u": USERNAME,
"m": 0, # Set to Osu default, can change if wanted.
"limit": NUMBER_OF_PLAYS
}

# Some helper functions

def get_weight(n):
    return pow(0.95, n)

def strip_unicode(string):
    stripped = ''.join(c for c in raw_text if c != '\\')
    return stripped

# Get best plays, limited to the config amount.
res = requests.get('https://osu.ppy.sh/api/get_user_best', params=payload).json()
beatmaps = [bmap['beatmap_id'] for bmap in res]
times = []
info = []

for idx in range(len(beatmaps)):
    try:
        payload2 = {
        "k": SECRET_KEY,
        "b": int(beatmaps[idx])
        }   
        timeres = requests.get('https://osu.ppy.sh/api/get_beatmaps', params=payload2)
        raw_text = timeres.text
        un_unicoded = strip_unicode(raw_text)
        jsonified = json.loads(un_unicoded)[0]
        times.append(int(jsonified['total_length']))
        info.append((jsonified['title'], jsonified['version']))
    except:
        print("Some beatmap is broken")

numerator = 0
denominator = 0
minseen = float('inf')
minseenidx = 0
maxseen = 0
maxseenidx = 0

for k in range(len(times)):
    if times[k] > maxseen:
        maxseen = times[k]
        maxseenidx = k
    if times[k] < minseen:
        minseen = times[k]
        minseenidx = k
    multiplier = get_weight(k)
    numerator += times[k] * multiplier
    denominator += multiplier

print("User: {}".format(payload["u"]))
print("Number of beatmaps analyzed: {}".format(len(times)))
print("Weighted average time (pp weighting): {}".format(numerator / denominator))
print("Unweighted average time: {}".format(sum(times) / len(times)))
print("The longest map in your top {} is {}, {}, and it is {} seconds long".format(len(times), info[maxseenidx][0], info[maxseenidx][1], maxseen))
print("The shortest map in your top {} is {}, {}, and it is {} seconds long".format(len(times), info[minseenidx][0], info[minseenidx][1], minseen))






