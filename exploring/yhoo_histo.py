from bs4 import BeautifulSoup
import re
import requests
import datetime
import json


today = datetime.datetime.now()
print today

r = requests.get("http://ichart.finance.yahoo.com/table.csv", params={'s' : 'GOOG', 'a' : str(today.month-1), 'b' : str(today.day), 'c': str(today.year-1), 'd' : str(today.year-1), 'e' : str(today.day), 'f' : str(today.year-1), 'g' : 'd', 'ignore' : '.csv'})
print r.url
csv_data = r.content


csv_data = csv_data.split('\n')
data_histo = []
for line in csv_data:
    #print line
    if (len(line)>0):
        data_histo.append(line.split(','))
        #print line.split(',')


data_histo = [data_histo[0]] + data_histo[:1:-1]
print data_histo


vec_date = []
vec_close = []
for i in range(1, len(data_histo)):
    
    if (i < len(data_histo)-1) and float(data_histo[i][0][5:7]) != float(data_histo[i+1][0][5:7]):
        vec_date.append(data_histo[i][0][-2:] + "-" + data_histo[i][0][5:7])
    else:
        vec_date.append('')
        
    vec_close.append(float(data_histo[i][-1]))


print vec_date
print vec_close


#print data_histo[:1:-1]

#print r.text
#soup = BeautifulSoup(r.text)
#print soup.title.string
#soup.find_all(id=re.compile("yfs_l84"))
#print soup.find_all('span')




import pygal

line_chart = pygal.Line(show_dots=False)
line_chart.title = 'GOOG 1y'
line_chart.x_labels =  vec_date
line_chart.add('GOOG', vec_close)
line_chart.render_to_file('yhoofin.svg')
#line_chart.render_to_png('blub.png')