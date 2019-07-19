import pymysql


class MySQL_DB:
	ip = ''
	user = ''
	pwd = ''
	database = ''

	DB = None
	CURSOR = None

	def __init__(self, ip, user, pwd, database):
		self.ip = ip
		self.user = user
		self.pwd = pwd
		self.database = database

		self.DB = pymysql.connect(ip, user, pwd, database, charset='utf8')
	
	def execute(self, sql):
		#print('todo save data to db')
		try:
			CURSOR = self.DB.cursor()
			CURSOR.execute(sql)
			data = CURSOR.fetchall()

			self.DB.commit()

			return data
		except Exception as e:
			print(e)
			self.DB.rollback()

	def __del__(self):
		self.DB.close()


"""
DB=None
CURSOR=None

def execute(sql):
	print('todo save data to db')
	CURSOR.execute(sql)
	data = CURSOR.fetchall()
	return data

def connect_db():
	print('todo connect to database')
	DB = pymysql.connect('localhost', 'drliu', 'drliu', 'on-sale_book', charset='utf8')
	CURSOR = DB.cursor()

def close_db():
	DB.close()
	print('todo close db connect')

def execute2(sql):
	print('todo save data to db')
	DB = pymysql.connect('localhost', 'drliu', 'drliu', 'on-sale_book', charset='utf8')
	CURSOR = DB.cursor()

	print(type(DB))
	print(type(CURSOR))

	CURSOR.execute(sql)
	data = CURSOR.fetchall()

	DB.close()

	return data
	"""