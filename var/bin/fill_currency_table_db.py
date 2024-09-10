#!/usr/bin/python

# Workarround Devops  Automate made By BILL
import psycopg2

#Fetch pine connection
conn = psycopg2.connect(
   database="pinegap_db", user='PINEGAP_DB_USER', password='PINEGAP_DB_PASSWD_TO_CHANGE', host='pinegap-database', port= '5432'
)
#Define a cursor object
cursor = conn.cursor()


#alter table Statement SQL
cursor.execute('''INSERT INTO public.currencies_currency(code,name,symbol,factor,is_active,is_base,is_default,info) VALUES ('BRL','REAL','R$','1',true,true,true,'1')''')
conn.commit()
print("Table (Currencies.currency) Filled successfully!!!")

#Unpine connection
conn.close()

