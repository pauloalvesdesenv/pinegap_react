#!/usr/bin/python
import psycopg2

# Workarround Devops  Automate made By BILL


#Fetch pine connection
conn = psycopg2.connect(
   database="pinegap_db", user='PINEGAP_DB_USER', password='PINEGAP_DB_PASSWD_TO_CHANGE', host='pinegap-database', port= '5432'
)
#Define a cursor object
cursor = conn.cursor()


#Create Intermediate column to Migrate column "financeiro")
sql ='''ALTER TABLE public.assets ADD COLUMN financeiro_temp numeric NULL;'''
cursor.execute(sql)

#Commit SQL post Changes
conn.commit()
print("Column Intermediate created  successfully!!!")


#Unpine connection
conn.close()
