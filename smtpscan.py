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
 
smtp_fingerprint_list = []
key_to_hosts = {}
for json_file in file_list:
 
    with open(json_file,"rb") as fd:
 
        scan_result = json.load(fd)
 
        if scan_result['smtpFingerprint']:
            print("%s => %s" % (scan_result['hiddenService'],scan_result['smtpFingerprint']))
            sql_select_query ="SELECT id from onion WHERE url=%s"
            value=scan_result['hiddenService'].rstrip()
            print(value)
            mycursor.execute(sql_select_query,(value,))
            record=mycursor.fetchall()

            for row in record:
                sql_select_query_status="SELECT * from smtps WHERE onion_id=%s"
                mycursor.execute(sql_select_query_status,(row[0],))
                counter=len(mycursor.fetchall())
                if counter==0:
                      sql_insert_query="INSERT INTO smtps (onion_id,smtpfingerprint,smtpbanner) VALUES (%s,%s,%s)"
                      val=(row[0],scan_result['smtpFingerprint'],scan_result['smtpBanner'])
                      mycursor.execute(sql_insert_query,val)
                      mydb.commit()
                      print("Valor insertado correctamente ",val)
