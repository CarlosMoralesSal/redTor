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

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
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
         r=requests.head("http://"+line.rstrip(),proxies=proxies, headers=random_headers())
         print(r.status_code)
         response = requests.get("http://"+line.rstrip(), proxies=proxies, headers=random_headers())
         #print(response)
         soup = BeautifulSoup(response.text, 'html.parser')
         for title in soup.find_all('title'):
           print(title.get_text())
           sql= "UPDATE onion SET title=%s,updated_at=%s,state=1 WHERE id=%s"
           val=(title.get_text(),now.strftime('%Y-%m-%d %H:%M:%S'),row[0])
           mycursor.execute(sql,val)
           mydb.commit()
           print("Valor actualizado correctamente ",val)
         meta = soup.find_all('meta')
         for tag in meta:
            if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['description']:
             print('CONTENT :', tag.attrs['content'])
             sql="UPDATE onion SET description=%s,updated_at=%s WHERE id=%s"
             val=(tag.attrs['content'],now.strftime('%Y-%m-%d %H:%M:%S'),row[0])
             mycursor.execute(sql,val)
             mydb.commit()
             print("Valor actualizado correctamente ",val)

   except:
     print("Error con ",line.rstrip())
     sql="UPDATE onion SET state=0,updated_at=%s WHERE id=%s"
     val=(now.strftime('%Y-%m-%d %H:%M:%S'),row[0])
     mycursor.execute(sql,val)
     mydb.commit()
     pass 
