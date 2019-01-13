import requests
import json
import datetime

from os import path
from os import makedirs

catalog_url="http://apis.juhe.cn/goodbook/catalog?key={}&dtype=json"
books_url="http://apis.juhe.cn/goodbook/query?catalog_id={}&pn={}&rn={}&dtype=json&key={}"

def get_catalog(url):
	'''
	获取图书分类
	'''

	print(url)

	if path.isfile("../data/catalog.json"):
		with open("../data/catalog.json", 'r') as file:
			result_json = json.load(file)
			result = result_json['result']
			print("data/catalog.json is exist!")
			file.close()
			return result

	doc = requests.get(url)
	catalog_json = json.loads(doc.text)
	resultcode=catalog_json['resultcode']
	reason=catalog_json['reason']
	result=catalog_json['result']
	#for catalog in result:
		#print(catalog['id'], catalog['catalog'])
	if reason == "success":
		with open('../data/catalog.json', 'w') as f:
			json.dump(catalog_json, f)
			f.close()
		return result

def get_catalog_detail(detail_url, catalog):
	'''
	获取各类图书
	:param detail_url:
	:return:
	'''
	print(detail_url)

	day_set=datetime.date.today()

	if not path.exists("../data/{}".format(catalog)):
		makedirs("../data/{}".format(catalog))
	if not path.exists("../data/{}/{}".format(catalog, day_set)):
		makedirs("../data/{}/{}".format(catalog, day_set))
	if path.isfile("../data/{}/{}/detail.json".format(catalog, day_set)):
		print("{}/{}/detail.json is exist !".format(catalog, day_set))
		return 0

	catalog_details = requests.get(detail_url)
	catalog_details_json = json.loads(catalog_details.text)
	resultcode = catalog_details_json['resultcode']
	reason = catalog_details_json['reason']
	if reason != 'Success':
		return -1
	with open("../data/{}/{}/detail.json".format(catalog, day_set), 'w') as f:
		json.dump(catalog_details_json, f)
		f.close()

	return 0

if __name__ == '__main__':
	#print(datetime.date.today())
	f=open('./key.config', 'r')
	key=f.readline(-1).split(':')[1]
	f.close()

	catalog_result = get_catalog(catalog_url.format(key))
	print(catalog_result)
	for catalog in catalog_result:
		get_catalog_detail(books_url.format(catalog['id'], 1, 50, key), catalog['catalog'])