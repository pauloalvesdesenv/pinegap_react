#!/usr/bin/python
import psycopg2

# Workarround Devops  Automate made By BILL


#Fetch pine connection
conn = psycopg2.connect(
   database="pinegap_db", user='PINEGAP_DB_USER', password='PINEGAP_DB_PASSWD_TO_CHANGE', host='pinegap-database', port= '5432'
)
#Define a cursor object
cursor = conn.cursor()

#Correction Currency table (DB)
sql ='''ALTER TABLE public.assets ADD COLUMN financeiro_currency character varying(50) NOT NULL DEFAULT 'BRL';'''
cursor.execute(sql)

#Commit SQL post Changes
conn.commit()
print("Add default_Currency' Column  in Asset table successfully!!!")


#Unpine connection
conn.close()
