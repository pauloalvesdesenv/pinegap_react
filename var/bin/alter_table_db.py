#!/usr/bin/python
import psycopg2

# Workarround Devops  Automate made By BILL


#Fetch pine connection
conn = psycopg2.connect(
   database="pinegap_db", user='PINEGAP_DB_USER', password='PINEGAP_DB_PASSWD_TO_CHANGE', host='pinegap-database', port= '5432'
)
#Define a cursor object
cursor = conn.cursor()

#alter table Statement SQL - (Set Financeiro to Numeric Data type Field)
sql ='''ALTER TABLE public.assets ALTER COLUMN financeiro TYPE NUMERIC coalesce(financeiro::text,'');'''

cursor.execute(sql)

print("Column 'Financeiro' Modified the (data type) to 'Numeric' successfully!!!")


#Commit SQL post Changes
conn.commit()


#Unpine connection
conn.close()
