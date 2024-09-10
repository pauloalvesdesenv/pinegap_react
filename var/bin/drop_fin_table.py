#!/usr/bin/python
import psycopg2

# Workarround Devops  Automate made By BILL


#Fetch pine connection
conn = psycopg2.connect(
   database="pinegap_db", user='PINEGAP_DB_USER', password='PINEGAP_DB_PASSWD_TO_CHANGE', host='pinegap-database', port= '5432'
)
#Define a cursor object
cursor = conn.cursor()


#Drop Column 'Financeiro'
sql ='''ALTER TABLE public.assets DROP COLUMN financeiro;'''
cursor.execute(sql)

#Commit SQL post Changes
conn.commit()
print(" The OLD 'Financeiro' Column droped Successfully!!!")


#Unpine connection
conn.close()

