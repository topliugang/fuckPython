 # -*- coding:utf-8 -*- 
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')

url = 'http://www.baidu.com/'
url2 = 'http://wanimal1983.tumblr.com/'

req = requests.get(url2)
page = req.text
print page.decode()



