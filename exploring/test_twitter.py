from bs4 import BeautifulSoup
import re
import requests
import json

r = requests.get("http://search.twitter.com/search.json", params={'q' : '$GOOG'})
#print r.url

#print r.text


j = json.loads(r.text)

for tweet in j['results']:
    print tweet['text']