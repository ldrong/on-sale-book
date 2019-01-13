import pymysql

DB=""
CURSOR=""

def execute(sql):
	print('todo save data to db')
	CURSOR.execute(sql)
	data = CURSOR.fetchall()
	return data

def connect_db():
	print('todo connect to database')
	DB = pymysql.connect('localhost', 'drliu', 'drliu', 'on-sale-book', charset='utf8')
	CURSOR = DB.cursor()

def close_db():
	DB.close()
	print('todo close db connect')