 # -*- coding:utf-8 -*- 
import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')

url = 'http://www.baidu.com/'
url2 = 'http://wanimal1983.tumblr.com/'

datas = {'key1':'value1', 'key2':'value2'}
req = requests.get(url, params=datas)
page = req.text
soup = BeautifulSoup(page, 'html.parser')



print req.cookies