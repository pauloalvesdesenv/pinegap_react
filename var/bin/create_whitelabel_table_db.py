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
cursor.execute('DROP TABLE IF EXISTS public.whitelabels')

#Create table Statement SQL
sql ='''CREATE TABLE public.whitelabels(
   "id" serial PRIMARY KEY,
   site_name varchar NOT NULL,
   academy_link varchar NOT NULL,
   browser_icon varchar NOT NULL,
   interface_icon varchar NOT NULL,
   interface_logo varchar NOT NULL,
   report_logo varchar NOT NULL
);'''

cursor.execute(sql)

#Commit SQL post Changes
conn.commit()

print("Whitelabel table created successfully.!!!!!")

#Unpine Connection
conn.close()

