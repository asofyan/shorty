#!/usr/bin/env python

import http
import sys
import os

# Flask Import
from flask import Flask, request, redirect, render_template, url_for
from flask import jsonify, abort, make_response

# import MySQLdb
import pymysql
#from importlib import reload

# Toekn and URL check import
from check_encode import random_token, url_check, check_prefix
from display_list import list_data

from sql_table import mysql_table

# Config import
#import config
from config import db_table,  db_db, db_host, db_passwrd, db_user, config_domain
from libs.web_url import WebUrl

# Import Loggers
import logging
from logging.handlers import RotatingFileHandler
from time import strftime
import traceback

from auth import auth
logger = logging.getLogger('tdm')

from blueprints import api
from libs import jatayu

# Setting UTF-8 encoding

# utf-8 is already set as string in python3
#reload(sys)
#sys.setdefaultencoding('UTF-8')
os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
app.config.from_object('config')

shorty_host = config_domain

# MySQL configurations

host = db_host
user = db_user
passwrd = db_passwrd
db = db_db

@app.route('/analytics/<short_url>')
def analytics(short_url):

	info_fetch, counter_fetch, browser_fetch, platform_fetch = list_data(
	    short_url)
	return render_template("data.html", host=shorty_host, info=info_fetch, counter=counter_fetch,
	 browser=browser_fetch, platform=platform_fetch)


@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def index():
	conn = pymysql.connect(db_host , db_user , db_passwrd , db_db)
	cursor = conn.cursor()

	# Return the full table to displat on index.
	list_sql = "SELECT * FROM %s;"%db_table
	cursor.execute(list_sql)
	result_all_fetch = cursor.fetchall()


	if request.method == 'POST':
		og_url = request.form.get('url_input')
		custom_suff = request.form.get('url_custom')
		tag_url = request.form.get('url_tag')
		if custom_suff == '':
			token_string =  random_token()
		else:
			token_string = custom_suff
		if og_url != '':
			#if url_check(og_url) == True:
			og_url = check_prefix(og_url)
			if og_url:
				# Check's for existing suffix
				check_row = "SELECT S_URL FROM WEB_URL WHERE S_URL = %s FOR UPDATE"
				cursor.execute(check_row,(token_string,))
				check_fetch = cursor.fetchone()

				if (check_fetch is None):
					insert_row = """
						INSERT INTO WEB_URL(URL , S_URL , TAG) VALUES( %s, %s , %s)
						"""
					result_cur = cursor.execute(insert_row ,(og_url , token_string , tag_url,))
					conn.commit()
					conn.close()
					e = ''
					return render_template('index.html' ,shorty_url = shorty_host+token_string , error = e )
				else:
					e = "The Custom suffix already exists . Please use another suffix or leave it blank for random suffix."
					return render_template('index.html' ,table = result_all_fetch, host = shorty_host,error = e)
			else:
				e = "URL entered doesn't seem valid , Enter a valid URL."
				return render_template('index.html' ,table = result_all_fetch, host = shorty_host,error = e)

		else:
			e = "Enter a URL."
			return render_template('index.html' , table = result_all_fetch, host = shorty_host,error = e)
	else:
		e = ''
		return render_template('index.html',table = result_all_fetch ,host = shorty_host, error = e )

# Rerouting funciton
@app.route('/<short_url>', methods=['GET'])
def reroute(short_url):
	conn = pymysql.connect(db_host , db_user , db_passwrd , db_db)
	web_url = WebUrl(conn)
	cursor = conn.cursor()
	platform = request.user_agent.platform
	browser =  request.user_agent.browser
	counter = 1

	# Platform , Browser vars
	browser_dict = {'firefox': 0 , 'chrome':0 , 'safari':0 , 'other':0}
	platforms_dict = {'windows':0 , 'iphone':0 , 'android':0 , 'linux':0 , 'macos':0 , 'other':0}

	# Analytics
	if browser in browser_dict:
		browser_dict[browser] += 1
	else:
		browser_dict['other'] += 1

	if platform in platforms_dict.keys():
		platforms_dict[platform] += 1
	else:
		platforms_dict['other'] += 1

	url = web_url.get_url_by_code(short_url)

	if url:
		web_url.update_counter(short_url, browser_dict, platforms_dict, counter)
		conn.close()
		return redirect(url), http.client.FOUND

	try:
		res = jatayu.get_referral_by_code(short_url.upper())
	except Exception as error:
		print(error)
		return jsonify({
			'error_message': 'Jatayu Connection Error',
		}), http.client.INTERNAL_SERVER_ERROR

	response = res.json()

	if res.status_code == http.client.NOT_FOUND:
		return render_template('404.html'), http.client.NOT_FOUND

	if res.status_code != http.client.OK:
		return jsonify({ 'error_message': 'Jatayu Internal Error', 'error': response}), http.client.INTERNAL_SERVER_ERROR

	url = 'https://nilaiku-rama.microaid.io/profile/' + response['uuid']


	return redirect(url), http.client.FOUND

# Search results
@app.route('/search' ,  methods=['GET' , 'POST'])
def search():
	s_tag = request.form.get('search_url')
	if s_tag == "":
		return render_template('index.html', error = "Please enter a search term")
	else:
		conn = pymysql.connect(host , user , passwrd, db)
		cursor = conn.cursor()

		search_tag_sql = "SELECT * FROM WEB_URL WHERE TAG = %s"
		cursor.execute(search_tag_sql , (s_tag, ) )
		search_tag_fetch = cursor.fetchall()
		conn.close()
		return render_template('search.html' , host = shorty_host , search_tag = s_tag , table = search_tag_fetch )


@app.after_request
def after_request(response):
	timestamp = strftime('[%Y-%b-%d %H:%M]')
	logger.error('%s %s %s %s %s %s',timestamp , request.remote_addr , \
				request.method , request.scheme , request.full_path , response.status)
	return response


@app.errorhandler(Exception)
def exceptions(e):
	tb = traceback.format_exc()
	timestamp = strftime('[%Y-%b-%d %H:%M]')
	logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
        timestamp, request.remote_addr, request.method,
        request.scheme, request.full_path, tb)
	return make_response(e , 405)


app.register_blueprint(api.mod, url_prefix='/api')

if __name__ == '__main__':

	# Logging handler
	handler = RotatingFileHandler('shorty.log' , maxBytes=100000 , backupCount = 3)
	logger.setLevel(logging.ERROR)
	logger.addHandler(handler)
	app.run(host='0.0.0.0' , port=5000)
