'''
	SQL Table Create Statement , 
	Follow the same order as given.
'''
from config import db_table

mysql_table = '''
		CREATE TABLE %s(
		ID INT AUTO_INCREMENT,
		URL VARCHAR(512),
		S_URL VARCHAR(80), 
		TAG VARCHAR(80),
		COUNTER INT DEFAULT 0,
		CHROME INT DEFAULT 0,
		FIREFOX INT DEFAULT 0,
		SAFARI INT DEFAULT 0,
		OTHER_BROWSER INT DEFAULT 0,
		ANDROID INT DEFAULT 0,
		IOS INT DEFAULT 0, 
		WINDOWS INT DEFAULT 0,
		LINUX INT DEFAULT 0,
		MAC INT DEFAULT 0,
		OTHER_PLATFORM INT DEFAULT 0 , 
		PRIMARY KEY(ID));
		'''
mysql_table = mysql_table % db_table
