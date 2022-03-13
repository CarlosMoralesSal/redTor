import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="onionalert"
)

mycursor = mydb.cursor()
with open('onion_list.txt') as file:
    for line in file:
        print(line.rstrip())
        sql_select_query ="SELECT * from onion WHERE url=%s"
        value=line.rstrip()
        mycursor.execute(sql_select_query,(value,))
        record=mycursor.fetchall()
        count=len(record)
        print(count)
        if count==0:
            sql= "INSERT INTO onion(url,state)VALUES(%s,%s)"
            val=(line.rstrip(),1)
            mycursor.execute(sql,val)
            mydb.commit()
            print("Valor insertado correctamente ",val)
