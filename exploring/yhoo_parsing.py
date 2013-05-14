from bs4 import BeautifulSoup
import re
import requests
import datetime

import utility

symbol = "GOOG"

r = requests.get("http://finance.yahoo.com/q", params={'s' : symbol})
soup = BeautifulSoup(r.text)


if (soup.title.string.find('Symbol Lookup from Yahoo') != -1):
    print 'invalid symbol'
else:
    #parsing
    for tag_prev_close in soup.find_all('th', text=re.compile("Prev Close:")):

        if utility.is_number(tag_prev_close.next_sibling.string):
            prev_close = float(tag_prev_close.next_sibling.string)
            print prev_close
            break
    
    
    for tag_last_price in soup.find('span', id='yfs_l84_' + symbol.lower()):
        if utility.is_number(tag_last_price.string):
            last_price = float(tag_last_price.string)
            print last_price
            break
    
    div_tag = soup.find('div', id='yfi_rt_quote_summary')
    print div_tag
            
    