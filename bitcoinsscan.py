import glob
import json
import shodan
import time
import mysql.connector 
import requests

bitcoinabuse_api=""
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="onionalert"
) 
file_list = glob.glob("onionscan_results/*.json")
mycursor = mydb.cursor()
 
bitcoin_list = []
bitcoin_to_mint = {}
for json_file in file_list:
 
    with open(json_file,"rb") as fd:
 
        scan_result = json.load(fd)
 
        if scan_result['identifierReport']['bitcoinAddresses']:
            print("%s => %s" % (scan_result['hiddenService'],scan_result['identifierReport']['bitcoinAddresses']))
        
            sql_select_query ="SELECT id from onion WHERE url=%s"
            value=scan_result['hiddenService'].rstrip()
            mycursor.execute(sql_select_query,(value,))
            record=mycursor.fetchall()
            for row in record:
                for addressbit in tuple(scan_result['identifierReport']['bitcoinAddresses']):
                   urladdress="https://www.bitcoinabuse.com/api/reports/check?api_token="+bitcoinabuse_api+"&address="+addressbit
                   response=requests.get(urladdress)
                   time.sleep(2)
                   bitcoinjson=response.json()

                   sql_insert_query="INSERT INTO cripto (onion_id,address,reported) VALUES (%s,%s,%s)"
                   val=(row[0],addressbit,bitcoinjson['count'])
                   mycursor.execute(sql_insert_query,val)
                   mydb.commit()
                   print("Valor insertado correctamente ",val)
            if tuple(scan_result['identifierReport']['bitcoinAddresses']) in bitcoin_to_mint:
                bitcoin_to_mint[tuple(scan_result['identifierReport']['bitcoinAddresses'])].append(scan_result['hiddenService'])
            else:
                bitcoin_to_mint[tuple(scan_result['identifierReport']['bitcoinAddresses'])] = [scan_result['hiddenService']]

for address in bitcoin_to_mint:
    
    if len(bitcoin_to_mint[address]) > 1:
        
        print("\n[!] Bitcoin Address {0} is used on multiple hidden services." .format(address))
        
        for key in bitcoin_to_mint[address]:
            
            print("\t%s" % key)

