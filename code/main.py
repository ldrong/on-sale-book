import requests
import json
import datetime

from os import path
from os import makedirs
import database as db

catalog_url="http://apis.juhe.cn/goodbook/catalog?key={}&dtype=json"
books_url="http://apis.juhe.cn/goodbook/query?catalog_id={}&pn={}&rn={}&dtype=json&key={}"

#连接mysql数据库
on_sale_book = db.MySQL_DB('localhost', 'drliu', 'drliu', 'on_sale_book')

def get_catalog(url):
	'''
	获取图书分类
	'''
	print(url)

	doc = requests.get(url)
	catalog_json = json.loads(doc.text)
	resultcode=catalog_json['resultcode']
	reason=catalog_json['reason']
	result=catalog_json['result']

	if reason != "success":
		print(str(reason) + str(result))
		return {}

	for catalog in result:
		#print(catalog['id'], catalog['catalog'])
		check_sql = "select * from book_catalog where catalog_id = %d" % (int(catalog['id']))
		add_sql = "insert into book_catalog(catalog_id, catalog_name) value(%d, '%s')" % (int(catalog['id']), catalog['catalog'])

		res = on_sale_book.execute(check_sql)

		if len(res) == 0:
			on_sale_book.execute(add_sql)

	return result

	"""
	if path.isfile("../data/catalog.json"):
		with open("../data/catalog.json", 'r') as file:
			result_json = json.load(file)
			result = result_json['result']
			print("data/catalog.json is exist!")
			file.close()
			return result

	if reason == "success":
		with open('../data/catalog.json', 'w') as f:
			json.dump(catalog_json, f)
			f.close()
		return result
	"""

def get_catalog_detail(detail_url, catalog):
	'''
	获取各类图书
	:param detail_url:
	:return:
	'''
	#print(detail_url)

	day_set=datetime.date.today()

	catalog_details = requests.get(detail_url)
	catalog_details_json = json.loads(catalog_details.text)

	resultcode = catalog_details_json['resultcode']
	reason = catalog_details_json['reason']

	if reason != 'Success':
		return -1

	results = catalog_details_json['result']
	data_detail = results['data']
	print(data_detail)

	for book in data_detail:
		check_sql = "select * from book_info where title='%s' and day='%s'" %(book['title'], day_set)
		add_sql = "insert into book_info(catalog_id, title, tags, sub1, sub2, img, online, reading, bytime, day) value(%d, '%s', '%s', '%s', '%s', '%s', '%s', %d, '%s', '%s')" % (
			int(catalog['id']),
			book['title'],
			book['tags'],
			book['sub1'],
			book['sub2'],
			book['img'],
			book['online'],
			int(book['reading'][:-3] if book['reading'][:-3] != '' else '0'),
			book['bytime'],
			day_set)

		print(check_sql + "\n" + add_sql)
		res = on_sale_book.execute(check_sql)
		#print(res)
		if len(res) == 0:
			on_sale_book.execute(add_sql)

	"""
	if not path.exists("../data/{}".format(catalog['catalog'])):
		makedirs("../data/{}".format(catalog['catalog']))
	if not path.exists("../data/{}/{}".format(catalog['catalog'], day_set)):
		makedirs("../data/{}/{}".format(catalog['catalog'], day_set))
	if path.isfile("../data/{}/{}/detail.json".format(catalog['catalog'], day_set)):
		print("{}/{}/detail.json is exist !".format(catalog['catalog'], day_set))
		return 0
	with open("../data/{}/{}/detail.json".format(catalog['catalog'], day_set), 'w') as f:
		json.dump(catalog_details_json, f)
		f.close()
	"""
	return 0

if __name__ == '__main__':
	f=open('./key.config', 'r')
	key=f.readline(-1).split(':')[1]
	f.close()

	catalog_result = get_catalog(catalog_url.format(key))
	print(catalog_result)
	for catalog in catalog_result:
		get_catalog_detail(books_url.format(catalog['id'], 1, 100, key), catalog)