import os

table_name = "WEB_URL"

# WTF config

WTF_CSRF_ENABLED = True
SECRET_KEY = 'the_very_secure_secret_security_key_that_no_will_ever_guess'

# MySQL Config


db_host = "localhost"
db_user = "root"
db_passwrd = "password"
db_db = "shorty"
db_table = "WEB_URL"

# Basic Auth Config
username = os.environ.get('HANOMAN_USERNAME', 'admin')
password = os.environ.get('HANOMAN_PASSWORD', '1234')

# Domain Host

'''
For now , use http as using https returns a bad error message ,
For https , use a SSL certificate. ( under works)
'''
config_domain = "http://localhost:5000/"

# copy the above constants to local_config.py
# to put your own configuration
try:
	from local_config import *
except:
	pass
