from stem.control import Controller
from stem import Signal
from threading import Timer
from threading import Event

import codecs
import json
import os
import random
import subprocess
import sys
import time


import argparse
import csv
import math
import re
import time
from datetime import datetime
from functools import reduce
from random import choice
from multiprocessing import Pool, cpu_count, current_process, freeze_support
from tqdm import tqdm

import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs
from urllib.parse import quote
from urllib.parse import unquote
from bs4 import BeautifulSoup
from urllib3.exceptions import ProtocolError
from lxml.html import fromstring
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="onionalert"
)


desktop_agents = [
    'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',  # Tor Browser for Windows and Linux
    'Mozilla/5.0 (Android 10; Mobile; rv:91.0) Gecko/91.0 Firefox/91.0',  # Tor Browser for Android
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) '
    'AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
]

def print_epilog():
     return

parser = argparse.ArgumentParser(epilog=print_epilog(), formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--proxy", default='localhost:9050', type=str, help="Set Tor proxy (default: 127.0.0.1:9050)")
args = parser.parse_args()
proxies = {'http': 'socks5h://{}'.format(args.proxy), 'https': 'socks5h://{}'.format(args.proxy)}

def random_headers():
    return {'User-Agent': choice(desktop_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

mycursor = mydb.cursor()
with open('onion_list.txt') as file:
 print("Entro") 
 for line in file:
   try:
     sql_select_query ="SELECT id from onion WHERE url=%s"
     value=line.rstrip()
     mycursor.execute(sql_select_query,(value,))
     record=mycursor.fetchall()
     count=len(record)
     print(count)
     now = datetime.now()
     if count>0:
      for row in record:
         r=requests.get("http://"+line.rstrip(),proxies=proxies, headers=random_headers())
         #print(r)
         #print(r.text)
         #response = requests.get("http://"+line.rstrip(), proxies=proxies, headers=random_headers())
         #print(response)
         doc=fromstring(r.text)
         #print(doc)
         #root = lxml.html.fromstring(r.text)
         #print("Esto es ",root)
         language_construct = doc.xpath("//html/@lang") # this xpath is reliable(in long-term), since this is a standard construct.
         print(language_construct)
         language = "Not found in page source"
         if language_construct:
            language = language_construct[0]
         print(language)
         sql="UPDATE onion SET lang=%s WHERE id=%s"
         val=(language,row[0])
         print(val)
         mycursor.execute(sql,val)
         mydb.commit()
         print("Valor actualizado correctamente")
   except:
     print("Error con ",line.rstrip())
     sql="UPDATE onion SET state=0,updated_at=%s WHERE id=%s"
     val=(now.strftime('%Y-%m-%d %H:%M:%S'),row[0])
     mycursor.execute(sql,val)
     mydb.commit()
     pass 
