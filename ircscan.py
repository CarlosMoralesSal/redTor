import glob
import json
import shodan
import time
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="onionalert"
)

file_list = glob.glob("onionscan_results/*.json")
mycursor = mydb.cursor()
for json_file in file_list:
 
    with open(json_file,"rb") as fd:
 
        scan_result = json.load(fd)
 
        if scan_result['ircDetected']:
            print("%s => %s" % (scan_result['hiddenService'],scan_result['ircDetected']))
            #sql_select_query ="SELECT id from onion WHERE url=%s"
            #value=scan_result['hiddenService'].rstrip()
            #mycursor.execute(sql_select_query,(value,))
            #record=mycursor.fetchall()
            #for row in record:
            #    sql_select_query_status="SELECT * from mod_status_apache WHERE onion_id=%s"
            #    mycursor.execute(sql_select_query_status,(row[0],))
            #    counter=len(mycursor.fetchall())
            #    if counter==0:
            #          sql_insert_query="INSERT INTO mod_status_apache(onion_id,apache_version) VALUES (%s,%s)"
            #          val=(row[0],scan_result['identifierReport']['serverVersion'])
            #          mycursor.execute(sql_insert_query,val)
            #          mydb.commit()
            #          print("Valor insertado correctamente ",val)



