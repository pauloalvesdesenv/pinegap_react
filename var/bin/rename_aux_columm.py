#!/usr/bin/python
import psycopg2

# Workarround Devops  Automate made By BILL


#Fetch pine connection
conn = psycopg2.connect(
   database="pinegap_db", user='PINEGAP_DB_USER', password='PINEGAP_DB_PASSWD_TO_CHANGE', host='pinegap-database', port= '5432'
)
#Define a cursor object
cursor = conn.cursor()

#Rename  Aux Intermediate Column to be 'Financeiro'
sql ='''ALTER TABLE public.assets RENAME COLUMN financeiro_temp TO financeiro;'''
cursor.execute(sql)
print("Column intermediated renamed to 'Financeiro'  successfully!!!")


#Commit SQL post Changes
conn.commit()


#Unpine connection
conn.close()
