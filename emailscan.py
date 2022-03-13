import glob
import json
import shodan
import time
import mysql.connector 
#shodan_client = shodan.Shodan("SxaULPrsq9QnWHCi70G66riC87JdQQCk")

try:
 mydb = mysql.connector.connect(
     host="localhost",
     user="root",
     password="",
     database="onionalert"
 )
 
 file_list = glob.glob("onionscan_results/*.json")
 mycursor = mydb.cursor()
 email_list = []
 email_to_mint = {}
 for json_file in file_list:
 
     with open(json_file,"rb") as fd:
 
         scan_result = json.load(fd)
  
         if scan_result['identifierReport']['emailAddresses']:
             print("%s => %s" % (scan_result['hiddenService'],scan_result['identifierReport']['emailAddresses']))
             
             sql_select_query = "SELECT id from onion WHERE url=%s"
             value=scan_result['hiddenService'].rstrip()
             mycursor.execute(sql_select_query,(value,))
             record=mycursor.fetchall()
             for row in record:
               sql_select_query_status="SELECT * from emails WHERE onion_id=%s"
               mycursor.execute(sql_select_query_status,(row[0],))
               counter=len(mycursor.fetchall())
             
               if counter==0:
                 for emails in scan_result['identifierReport']['emailAddresses']:
                    sql_insert_query="INSERT INTO emails(onion_id,email)VALUES(%s,%s)"
                    print("Se va a insertar ",emails)
                    val=(row[0],emails)
                    mycursor.execute(sql_insert_query,val)
                    mydb.commit()
                    print("Valor insertado correctamente",val)
except mysql.connector.Error as error:
    print(error)

