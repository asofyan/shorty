# Script to build mysql table

from config import db_host, db_user, db_passwrd, db_db 
import pymysql
from sql_table import mysql_table

'''
Create_table.py looks for MySQL Config in config.py 
Creates a connection to the database using the supplied config

Creates a TABLE named WEB_URL with the specified rows.
Needs to RUN once when setting up the application on local or
web server.

You need to have a database already defined ( SHORTY for e.g is 
already present .).
'''

create_table = mysql_table
conn = pymysql.connect(db_host , db_user , db_passwrd, db_db)
cursor = conn.cursor()
cursor.execute(create_table)

conn.close()
