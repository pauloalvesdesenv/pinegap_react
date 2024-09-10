#!/usr/bin/python
import psycopg2

# Workarround Devops  Automate made By BILL


#Fetch pine connection
conn = psycopg2.connect(
   database="pinegap_db", user='PINEGAP_DB_USER', password='PINEGAP_DB_PASSWD_TO_CHANGE', host='pinegap-database', port= '5432'
)
#Define a cursor object
cursor = conn.cursor()

# Check if Table Exist
cursor.execute('DROP TABLE IF EXISTS public.currencies_currency')

#Create table Statement SQL
sql ='''CREATE TABLE public.currencies_currency(
   code varchar NULL,
   "name" varchar NULL,
   symbol varchar NULL,
   factor varchar NULL,
   is_active bool NULL,
   is_base bool NULL,
   is_default bool NULL,
);'''

cursor.execute(sql)

#Commit SQL post Changes
conn.commit()

print("Currency table created successfully.!!!!!")

#Unpine Connection
conn.close()

