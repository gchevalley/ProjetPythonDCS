from bs4 import BeautifulSoup
import re #regex
import requests
import datetime
import json
import sys

import utility


class Ticker():
    def __init__(self, symbol, bypass_histo_data = False):
        self.symbol = symbol.upper()
        self.twitter_symbol = "$" + self.symbol
        self.company_name = ""
        self.is_valid = False
        self.last_price = -1
        self.previous_close = -1
        self.daily_return = 0
        self.today_open = -1
        self.today_high = -1
        self.today_low = -1
        self.high_52w = -1
        self.low_52w = -1
        self.acutal_bid = -1
        self.actual_ask = -1
        self.yahoo_1yr_target_price = -1
        self.beta = -1
        self.next_earnings_date = '#N/A'
        self.pe = "#N/A"
        self.eps = "#N/A"
        self.div_yield = -1
        self.market_cap = "#N/A"
        
        self.histo_data = []
        self.path_chart_1yr = ""
        
        self.relate_tweet = []
        
        self.in_monitor = False
        self.alerts = []
        
        self.logs = []
        
        
        self.logs.append([datetime.datetime.now(), "init"])
        self.download_last_datas_from_yahoo()
        
        if bypass_histo_data == False:
            self.download_histo_data_from_yahoo()
            self.generate_chart()
            self.download_related_tweet()
    
    
    def download_last_datas_from_yahoo(self):
        """recupere les donnees live"""
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
            
            for tag_prev_close in soup.find_all('th', text=re.compile("Prev Close:")):
                if utility.is_number(tag_prev_close.next_sibling.string):
                    self.previous_close = float(tag_prev_close.next_sibling.string)
                    self.daily_return = round(100*((self.last_price/self.previous_close)-1),2)
                    
                    break
            
            self.company_name = soup.find('div', id='yfi_rt_quote_summary').find('h2').string
            
            for tag_beta in soup.find_all('th', text=re.compile("Beta:")):
                if utility.is_number(tag_beta.next_sibling.string):
                    self.beta = float(tag_beta.next_sibling.string)
                    break
            
            for tag_ern in soup.find_all('th', text=re.compile('Next Earnings Date:')):
                if tag_ern.next_sibling.text != '':
                    self.next_earnings_date = tag_ern.next_sibling.text
                    break
            
            for tag_market_cap in soup.find_all('span', id='yfs_j10_' + self.symbol.lower()):
                if utility.is_number(tag_market_cap.string[:-1]):
                    self.market_cap = tag_market_cap.string
                    break
            
            
            for ttm_span in soup.find_all('span', text=re.compile('ttm')):
                
                if ttm_span.parent.text[:3] == 'P/E':
                    if utility.is_number(ttm_span.parent.next_sibling.text):
                        self.pe = float(ttm_span.parent.next_sibling.text)
                elif ttm_span.parent.text[:3] == 'EPS':
                    if utility.is_number(ttm_span.parent.next_sibling.text):
                        self.eps = float(ttm_span.parent.next_sibling.text)
                
                
            
                
    def download_histo_data_from_yahoo(self, date_from = datetime.date(datetime.datetime.now().year-1, datetime.datetime.now().month, datetime.datetime.now().day), date_to = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)):
        """recupere les donnees historiques"""

        
        if self.is_valid:
            r = requests.get("http://ichart.finance.yahoo.com/table.csv", params={'s' : self.symbol, 'a' : str(date_from.month-1), 'b' : str(date_from.day), 'c': str(date_from.year), 'd' : str(date_to.month-1), 'e' : str(date_to.day), 'f' : str(date_to.year), 'g' : 'd', 'ignore' : '.csv'})
            
            csv_data = r.content
            csv_data = csv_data.split('\n')
            data_histo = []
            
            if (len(csv_data)>0): #check data are available
                for line in csv_data:
                    if (len(line)>0): #sometimes, last line is empty
                        data_histo.append(line.split(','))
                
                data_histo = [data_histo[0]] + data_histo[:1:-1] #headers + reverse timeserie
                
                #cast
                for i in range(1, len(data_histo)): #saute premiere ligne car header
                    for j in range(1, len(data_histo[i])): #saute premiere colonne car date
                        if utility.is_number(data_histo[i][j]):
                            data_histo[i][j] = float(data_histo[i][j])
                
                self.histo_data = data_histo
                
                self.logs.append([datetime.datetime.now(), "found histo datas on yahoo finance " + str(len(csv_data)-1) + " entries"])
    
    
    def generate_chart(self):
        """creation du linechart sous forme d image png grace aux donnees historiques"""
        if self.is_valid and len(self.histo_data) > 10:
            
            from pygooglechart import Chart
            from pygooglechart import SimpleLineChart
            from pygooglechart import Axis
            
            price_max = -sys.maxint
            price_min = sys.maxint
            
            vec_price = []
            vec_date = []
            
            for i in range(1, len(self.histo_data)):
                
                if (i < len(self.histo_data)-1) and float(self.histo_data[i][0][5:7]) != float(self.histo_data[i+1][0][5:7]): #end of month ?
                    vec_date.append(self.histo_data[i][0][5:7])
                else:
                    vec_date.append('')
                
                
                if utility.is_number(self.histo_data[i][6]):
                    
                    vec_price.append(self.histo_data[i][6])
                    
                    if self.histo_data[i][6] < price_min:
                        price_min = self.histo_data[i][6]
                    
                    if self.histo_data[i][6] > price_max:
                        price_max = self.histo_data[i][6]
            
            
            y_scale_up = int(price_max)
            y_scale_down = int(price_min)
            
            if y_scale_up-y_scale_down > 500:
                base = 100
            elif y_scale_up-y_scale_down > 200:
                base = 50
            else:
                base = 25
            
            for i in range(1,base+1):
                if ((y_scale_up + i) % base) == 0:
                    y_scale_up = y_scale_up+i
                    break
            
            for i in range(1,base+1):
                if ((y_scale_down - i) % base) == 0:
                    y_scale_down -= i
                    break
            
            
            chart = SimpleLineChart(200, 125, y_range=[y_scale_down, y_scale_up])
            chart.add_data(vec_price)
            chart.set_colours(['0000FF'])
            left_axis = range(y_scale_down, y_scale_up + 1, base)
            chart.set_axis_labels(Axis.LEFT, left_axis)
            chart.set_axis_labels(Axis.BOTTOM, vec_date)
            
            
            utility.create_missing_folder(utility.FOLDER_CHART)
            
            chart.download(utility.FOLDER_CHART + '/' + self.symbol + '.png')
            self.path_chart_1yr = utility.FOLDER_CHART + '/' + self.symbol + '.png'
    
    
    def download_related_tweet(self):
        """recupere les derniers tweets ou l on trouve le $ticker de la societe"""
        if self.is_valid:
            r = requests.get("http://search.twitter.com/search.json", params={'q' : self.twitter_symbol})
            
            j = json.loads(r.text)
            
            for tweet in j['results']:
                self.relate_tweet.append(tweet['text'])
            
            self.logs.append([datetime.datetime.now(), "found tweets"])