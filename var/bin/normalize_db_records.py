
#!/usr/bin/python
import psycopg2
# Workarround Devops  Automate made By BILL


#Fetch pine connection
conn = psycopg2.connect(
   database="pinegap_db", user='PINEGAP_DB_USER', password='PINEGAP_DB_PASSWD_TO_CHANGE', host='pinegap-database', port= '5432'
)
#Define a cursor object
cursor = conn.cursor()


#Normalize Records Inconsistents  SQL - (Set Financeiro to Zero Value )
sql = '''update public.assets set financeiro = regexp_replace(financeiro, '[^0-9]*', '', 'g') ;'''
cursor.execute(sql)

#Commit SQL post Changes
conn.commit()
print("Table Field 'Financeiro' Correction Any inconsistence Value successfully!!!")


#Unpine connection
conn.close()

