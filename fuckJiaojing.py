# -*- coding:utf-8 -*-  
import urllib
import urllib2
from bs4 import BeautifulSoup
import bs4
import json

def getpage():
	url = 'http://218.59.228.162/wscgsxxcx/jdcwfcx.do'
	data = {'hpzl':'02', 'fzjg':'D', 'hphm':'k6506', 'clsbdh':'071433', 'type':'wfcx'}
	dataEncode = urllib.urlencode(data)
	page = urllib2.urlopen(url=url, data=dataEncode)
	return page.read()

def parsepage(page):
	soup = BeautifulSoup(page, 'html.parser')
	tables = soup.find_all("table", class_="wfresult")#tables 违章记录数组
	for table in tables:
		trs = table.find_all("tr")
		for tr in trs:
			print '##############tr####################'
			tds =  tr.children
			#print u'子节点的个数',len(tds)
			print type(tds)
			for td in tds:
				if not isinstance(td, bs4.element.NavigableString):#判断类型是否为
					print u'子节点类型为',type(td),u'内容为',td
			print '###############tr#####################'
			print



if __name__ == "__main__":
	parsepage(getpage()) 