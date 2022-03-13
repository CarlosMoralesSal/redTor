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

mycursor = mydb.cursor()
print("***********Dashboard de resumen***********************")
sql_select_query_status="SELECT count(*) from onion"
mycursor.execute(sql_select_query_status)
counter=mycursor.fetchone()
print("Onions Cargadas en la lista: ",counter[0])
sql_select_query_status="SELECT count(*) from smtps"
mycursor.execute(sql_select_query_status)
counter=mycursor.fetchone()
print("SMTPS encontrados: ",counter[0])
sql_select_query_status="SELECT count(distinct(sshkey)) from sshkey"
mycursor.execute(sql_select_query_status)
counter=mycursor.fetchone()
print("SSH Keys encontradas diferentes: ",counter[0])
sql_select_query_status="SELECT count(*) from mod_status_apache"
mycursor.execute(sql_select_query_status)
counter=mycursor.fetchone()
print("Onions con server apache afectado por mod_status: ",counter[0])
sql_select_query_status="SELECT count(distinct(address)) from cripto"
mycursor.execute(sql_select_query_status)
counter=mycursor.fetchone()
print("Wallets encontradas diferentes: ",counter[0])
sql_select_query_status="SELECT count(distinct(email)) from emails"
mycursor.execute(sql_select_query_status)
counter=mycursor.fetchone()
print("Emails encontrados diferentes: ",counter[0])
sql_select_query_status="SELECT count(*) from exifs"
mycursor.execute(sql_select_query_status)
counter=mycursor.fetchone()
print("Objetos encontrados con metadatos: ",counter[0])
sql_select_query_status="SELECT count(distinct(ip)) from ips"
mycursor.execute(sql_select_query_status)
counter=mycursor.fetchone()
print("Direcciones IPs diferentes: ",counter[0])
