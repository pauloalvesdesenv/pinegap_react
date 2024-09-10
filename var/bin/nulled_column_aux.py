#!/usr/bin/python
import psycopg2

# Workarround Devops  Automate made By BILL


#Fetch pine connection
conn = psycopg2.connect(
   database="pinegap_db", user='PINEGAP_DB_USER', password='PINEGAP_DB_PASSWD_TO_CHANGE', host='pinegap-database', port= '5432'
)
#Define a cursor object
cursor = conn.cursor()

#Nulled 'intermediate' column (asset table)
sql ='''ALTER TABLE public.assets ALTER COLUMN financeiro_temp DROP NOT NULL;'''
cursor.execute(sql)

print("Nulled Intermediate Column data structure  successfully!!!")


#Commit SQL post Changes
conn.commit()


#Unpine connection
conn.close()
