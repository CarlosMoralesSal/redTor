import json
import requests
import urllib
import json
import time

z = 0
i = 0
firstpart = "https://blockchain.info/rawaddr/"
bitcoinabuse = "https://www.bitcoinabuse.com/api/reports/check?api_token=UZQlbEyzIreuuaD6Nc42iGI98ZOqh5PqKb4Jjov2SQnedZajF39WZIpuAp9k&address="
initialinput = input("please type the 'seed' address: ")
initialreq = firstpart + initialinput
firstjson="https://blockchain.info/rawaddr/"
#firstjson = (requests.get(initialreq)).json()
firstjson = json.load(urllib.request.urlopen(initialreq))
#print(firstjson)
graphvizlines = []

addresslist = []
usedaddresslist = []

addresslist.append(initialinput)
usedaddresslist.append(initialinput)

while i < 6:
    if z == 1:
        initialreq = firstpart + addresslist[i]
        #print("La primera es: "+initialreq)
        #firstjson = (requests.get(initialreq)).json()
        firstjson = json.load(urllib.request.urlopen(initialreq))
        time.sleep(10)
    for transaction in firstjson["txs"]:
        payerlist = []
        recipientlist = []
        
        print("\nTransaccion: " + transaction["hash"])

        for item in transaction["inputs"]:
            payerlist.append(item["prev_out"]["addr"])
            if item["prev_out"]["addr"] not in addresslist:
                addresslist.append(item["prev_out"]["addr"])

        for target in transaction["out"]:
            recipientlist.append(target["addr"])
            if target["addr"] not in addresslist:
                addresslist.append(target["addr"])

        for payer in payerlist:
            for recipient in recipientlist:
                a = '"' + payer + '"' + " -> " + '"' + recipient + '"' + ";"
                if a not in graphvizlines:
                    graphvizlines.append(a)
                    bitcoinreq=bitcoinabuse+payer
                    bitcoinjson = json.load(urllib.request.urlopen(bitcoinreq))
                    time.sleep(10)
                    print(bitcoinjson)
    i = i + 1    
    z = 1
        

for t in graphvizlines:
    print(t)
