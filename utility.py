import urllib2 
import requests
import os

DB_NAME = 'ppdcs.sql3'
FOLDER_CHART = "img_chart"

def check_internet_connection(check_url = 'http://www.google.com'):
    try:
        requests.get(check_url)
        return True
    except requests.exceptions.ConnectionError, e:
        return False


def check_internet_connection_old(check_url = 'http://www.google.com'): #deprecie
    try:
        urllib2.urlopen(check_url)
        return True
    except urllib2.URLError, e:
        return False


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def create_missing_folder(d): #http://stackoverflow.com/questions/273192/python-best-way-to-create-directory-if-it-doesnt-exist-for-file-write
    if not os.path.exists(d):
        os.makedirs(d)
    
def average(vec):
    sum = 0.0
    k = 0
    for item in vec:
        sum += item
        k += 1
    
    if k > 0:
        return sum/k
    else:
        return 0.0