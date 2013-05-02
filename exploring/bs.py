from bs4 import BeautifulSoup

import re

html_doc = """
<html><head><title>The Dormouse's story</title></head>

<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc)

#print(soup.prettify())



#print soup.title #tag + contenu
#print soup.title.name # nom du tag
#print soup.title.string # contenu du tag
#print soup.title.parent.name #nom du tag au dessus de la hierchie

#print soup.b.parent.string

#print soup.p
#print soup.p['class']
#print soup.a
#print soup.find_all('a')
#print soup.find(id="link3")

print soup.find_all(href=re.compile("elsie"), id='link1')