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
 
        if scan_result['mongodbDetected']:
            print("%s => %s" % (scan_result['hiddenService'],scan_result['mongodbDetected']))
            



