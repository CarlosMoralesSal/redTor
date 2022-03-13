import glob
import json
import shodan
import time
import mysql.connector 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="onionalert"
)  
shodan_client = shodan.Shodan("")
mycursor = mydb.cursor() 
file_list = glob.glob("onionscan_results/*.json")
 
ftp_fingerprint_list = []
key_to_hosts = {}
for json_file in file_list:
 
    with open(json_file,"rb") as fd:
 
        scan_result = json.load(fd)
 
        if scan_result['ftpFingerprint']:
            print("%s => %s" % (scan_result['hiddenService'],scan_result['ftpFingerprint']))
            sql_select_query ="SELECT id from onion WHERE url=%s"
            value=scan_result['hiddenService'].rstrip()
            mycursor.execute(sql_select_query,(value,))
            record=mycursor.fetchall()
            if scan_result['ftpFingerprint'] in key_to_hosts:
                key_to_hosts[scan_result['ftpFingerprint']].append(scan_result['hiddenService'])
            else:
                key_to_hosts[scan_result['ftpFingerprint']] = [scan_result['hiddenService']]



for ftp_fingerprint in key_to_hosts:
    
    if len(key_to_hosts[ftp_fingerprint]) > 1:
        
        print("[!] ftp fingerprint %s is used on multiple hidden services." % ftp_fingerprint)
        
        for key in key_to_hosts[ftp_fingerprint]:
            
            print("\t%s" % key)

    while True:
    
        try:
            
            shodan_result = shodan_client.search(ftp_fingerprint)
            break
        except:
            time.sleep(5)
            pass
        
    if shodan_result['total'] > 0:

        for hit in shodan_result['matches']:
            print("[!] Hit for %s on %s for hidden services %s" % (ftp_fingerprint,hit['ip_str'],",".join(key_to_hosts[ftp_fingerprint])))
