from bs4 import BeautifulSoup
import re
import requests
import datetime
import json

import utility


class Ticker():
    def __init__(self, symbol):
        self.symbol = symbol.upper()
        self.twitter_symbol = "$" + self.symbol
        self.is_valid = False
        self.last_price = -1
        self.previous_close = -1
        self.today_open = -1
        self.today_high = -1
        self.today_low = -1
        self.high_52w = -1
        self.low_52w = -1
        self.acutal_bid = -1
        self.actual_ask = -1
        self.yahoo_1yr_target_price = -1
        self.beta = -1
        self.next_earnings_date = ''
        self.pe = -1
        self.eps = -1
        self.div_yield = -1
        
        self.histo_data = []
        
        self.relate_tweet = []
        
        self.in_monitor = False
        self.alerts = []
        
        self.logs = []
        
        
        self.logs.append([datetime.datetime.now(), "init"])
        
        self.download_last_datas_from_yahoo()
        self.download_histo_data_from_yahoo()
        self.download_related_tweet()
    
    
    def download_last_datas_from_yahoo(self):
        
        r = requests.get("http://finance.yahoo.com/q", params={'s' : self.symbol})
        soup = BeautifulSoup(r.text)
        
        if (soup.title.string.find('Symbol Lookup from Yahoo') != -1):
            #invalid symbol
            self.is_valid = False
            self.logs.append([datetime.datetime.now(), "invalid ticker"])
        else:
            self.is_valid = True
            self.logs.append([datetime.datetime.now(), "ticker seems valid"])
            
            #parse html pour recup value
            for tag_last_price in soup.find('span', id='yfs_l84_' + self.symbol.lower()):
                if utility.is_number(tag_last_price.string):
                    self.last_price = float(tag_last_price.string)
                    self.logs.append([datetime.datetime.now(), "found last price on yahoo finance"])
                    break
                
    def download_histo_data_from_yahoo(self, date_from = datetime.date(datetime.datetime.now().year-1, datetime.datetime.now().month, datetime.datetime.now().day), date_to = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)):
        #print date_from
        #print date_to
        
        if self.is_valid:
            r = requests.get("http://ichart.finance.yahoo.com/table.csv", params={'s' : self.symbol, 'a' : str(date_from.month-1), 'b' : str(date_from.day), 'c': str(date_from.year), 'd' : str(date_to.month-1), 'e' : str(date_to.day), 'f' : str(date_to.year), 'g' : 'd', 'ignore' : '.csv'})
            #print r.url
            
            csv_data = r.content
            csv_data = csv_data.split('\n')
            data_histo = []
            
            if (len(csv_data)>0): #check data are available
                for line in csv_data:
                    if (len(line)>0): #sometime, last line is empty
                        data_histo.append(line.split(','))
                
                data_histo = [data_histo[0]] + data_histo[:1:-1] #headers + reverse timeserie
                self.histo_data = data_histo
                
                self.logs.append([datetime.datetime.now(), "found histo datas on yahoo finance " + str(len(csv_data)-1) + " entries"])
                
    def download_related_tweet(self):
        if self.is_valid:
            r = requests.get("http://search.twitter.com/search.json", params={'q' : self.twitter_symbol})
            
            j = json.loads(r.text)
            
            for tweet in j['results']:
                self.relate_tweet.append(tweet['text'])
            
            self.logs.append([datetime.datetime.now(), "found tweets"])
