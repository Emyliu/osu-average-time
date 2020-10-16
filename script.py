import requests
import json
import unidecode
import re

# This script uses the Osu API V1 because the V2 OAuth endpoint is busted...

# Config 
SECRET_KEY: "ENTER SECRET KEY"
USERNAME: "ENTER USERNAME"
NUMBER_OF_PLAYS: 40

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

for idx in range(len(beatmaps)):
    payload2 = {
    "k": SECRET_KEY,
    "b": int(beatmaps[idx])
    }   
    timeres = requests.get('https://osu.ppy.sh/api/get_beatmaps', params=payload2)
    raw_text = timeres.text
    un_unicoded = strip_unicode(raw_text)
    times.append(int(json.loads(un_unicoded)[0]['total_length']))

numerator = 0
denominator = 0

for k in range(len(times)):
    multiplier = get_weight(k)
    numerator += times[k] * multiplier
    denominator += multiplier

print("User: {}".format(payload["u"]))
print("Number of beatmaps analyzed: {}".format(len(times)))
print("Average time: {}".format(numerator / denominator))





