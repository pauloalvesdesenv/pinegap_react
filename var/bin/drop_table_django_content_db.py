#!/usr/bin/python
import psycopg2

# Workarround Devops  Automate made By BILL


#Fetch pine connection
conn = psycopg2.connect(
   database="pinegap_db", user='PINEGAP_DB_USER', password='PINEGAP_DB_PASSWD_TO_CHANGE', host='pinegap-database', port= '5432'
)
#Define a cursor object
cursor = conn.cursor()


#Drop Table Django Content
sql ='''DROP TABLE public.django_content_type;'''
cursor.execute(sql)

#Commit SQL post Changes
conn.commit()
print(" 'Django Content Type' Table droped Successfully!!!")


#Unpine connection
conn.close()
