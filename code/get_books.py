import requests
import os
import time
import json
#from urllib2 import urlopen

catalog_url="http://apis.juhe.cn/goodbook/catalog?key=none&dtype=json"
books_url="http://apis.juhe.cn/goodbook/query?catalog_id={}&pn={}&rn={}&dtype=json&key=none"

def get_catalog(url):
	'''
	获取图书分类
	'''
	doc = requests.get(url)
	print(doc.text)

	catalog_json = json.loads(doc.text)
	resultcode=catalog_json['resultcode']
	reason=catalog_json['reason']
	result=catalog_json['result']
	#for catalog in result:
		#print(catalog['id'], catalog['catalog'])

	if reason == "success":
		return result

def get_catalog_detail(url):
	'''
	获取各类图书
	:param url:
	:return:
	'''

	print(url)
	catalog_details = requests.get(url)

	catalog_details_json = json.loads(catalog_details.text)
	resultcode = catalog_details_json['resultcode']
	reason = catalog_details_json['reason']

	if reason != 'Success':
		return -1

	catalog_details_data = catalog_details_json['result']['data']
	catalog_details_data_length = catalog_details_json['result']['totalNum']

	for book in catalog_details_data:
		print(book['title'], book['catalog'],
			  book['tags'], book['sub1'],
			  book['reading'], book['online'],
			  book['bytime'])

if __name__ == '__main__':
	catalog_result = get_catalog(catalog_url)
	for catalog in catalog_result:
		get_catalog_detail(books_url.format(catalog['id'],1,20))