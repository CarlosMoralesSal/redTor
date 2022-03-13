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

file_list = glob.glob("onionscan_results/*.json")
mycursor = mydb.cursor()
for json_file in file_list:
 
    with open(json_file,"rb") as fd:
 
        scan_result = json.load(fd)
 
        if scan_result['identifierReport']['exifImages']:
            print("%s => %s" % (scan_result['hiddenService'],scan_result['identifierReport']['exifImages']))
            sql_select_query ="SELECT id from onion WHERE url=%s"
            value=scan_result['hiddenService'].rstrip()
            mycursor.execute(sql_select_query,(value,))
            record=mycursor.fetchall()
            for row in record:
                sql_select_query_status="SELECT * from exifs WHERE onion_id=%s"
                mycursor.execute(sql_select_query_status,(row[0],))
                counter=len(mycursor.fetchall())
                if counter==0:
                      sql_insert_query="INSERT INTO exifs(onion_id,location) VALUES (%s,%s)"
                     
                      for i in range(len(scan_result['identifierReport']['exifImages'])):
                        
                        exifs=scan_result['identifierReport']['exifImages'][:i+1][i]
                      
                        val=(row[0],exifs['location'])
                        mycursor.execute(sql_insert_query,val)
                        mydb.commit()

                        v=exifs['exifTags']

                        last_id=mycursor.lastrowid
                        if len(v)>0:
                          for r in range(len(v)):

                           name=v[:r+1][r]['name']
                           values=v[:r+1][r]['value']
                           sql_insert_query_2="INSERT INTO exifdata(location_id,name,value) VALUES (%s,%s,%s)"
                           vals=(last_id,name,values)
                           mycursor.execute(sql_insert_query_2,vals)
                           mydb.commit()




