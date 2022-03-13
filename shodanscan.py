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
shodan_client = shodan.Shodan("SxaULPrsq9QnWHCi70G66riC87JdQQCk")
mycursor = mydb.cursor() 
file_list = glob.glob("onionscan_results/*.json")
 
ssh_key_list = []
key_to_hosts = {}
for json_file in file_list:
    with open(json_file,"rb") as fd:
        scan_result = json.load(fd)
 
        if scan_result['sshKey']:
            print("%s => %s" % (scan_result['hiddenService'],scan_result['sshKey']))
            sql_select_query ="SELECT id from onion WHERE url=%s"
            value=scan_result['hiddenService'].rstrip()
            mycursor.execute(sql_select_query,(value,))
            record=mycursor.fetchall()
            if scan_result['sshKey'] in key_to_hosts:
                key_to_hosts[scan_result['sshKey']].append(scan_result['hiddenService'])
            else:
                key_to_hosts[scan_result['sshKey']] = [scan_result['hiddenService']]

            for row in record:
                sql_select_subquery="SELECT id from sshkey where onion_id=%s and sshkey like %s"
                val=(row[0],scan_result['sshKey'])
                print(val)
                mycursor.execute(sql_select_subquery,val)
                r=mycursor.fetchall()
                print(len(r))
                if len(r)==0:
                   sql_insert_query="INSERT INTO sshkey (onion_id,sshkey) VALUES (%s,%s)"
                   val=(row[0],scan_result['sshKey'])
                   mycursor.execute(sql_insert_query,val)
                   mydb.commit()

for ssh_key in key_to_hosts:
    
    if len(key_to_hosts[ssh_key]) > 1:
        
        print("[!] SSH Key %s is used on multiple hidden services." % ssh_key)
        
        for key in key_to_hosts[ssh_key]:
            
            print("\t%s" % key)

    while True:
    
        try:
            
            shodan_result = shodan_client.search(ssh_key)
            break
        except:
            time.sleep(5)
            pass
        
    if shodan_result['total'] > 0:

        for hit in shodan_result['matches']:
            print("[!] Hit for %s on %s for hidden services %s" % (ssh_key,hit['ip_str'],",".join(key_to_hosts[ssh_key])))
            from ipwhois import IPWhois
            obj = IPWhois(hit['ip_str'])
            print(obj)
            response = obj.lookup_whois()

            details = response['nets'][0]
            print(details)
            print(row[0])
            cidr = details['cidr']
            name = details['name']
            city = details['city']
            state = details['state']
            country = details['country']
            address = details['address']
            description = details['description']
            
            sql_select_query ="SELECT id from sshkey WHERE sshkey like %s"
            value=ssh_key
            mycursor.execute(sql_select_query,(value,))
            record=mycursor.fetchall()
            print(record)
            if len(record)>0:
             for fila in record:
                sql_insert_query="INSERT INTO ips (onion_id,sshkey_id,ip,name,city,state,country,address,description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val=(row[0],fila[0],hit['ip_str'],name,city,state,country,address,description)
                mycursor.execute(sql_insert_query,val)
                mydb.commit()
