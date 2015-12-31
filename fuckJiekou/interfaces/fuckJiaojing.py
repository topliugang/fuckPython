# -*- coding:utf-8 -*-  
import urllib
import urllib2
from bs4 import BeautifulSoup
import bs4
import json

def getpage():
	url = 'http://218.59.228.162/wscgsxxcx/jdcwfcx.do'
	data = {'hpzl':'02', 'fzjg':'d', 'hphm':'k6506', 'clsbdh':'071433', 'type':'wfcx'}
	dataEncode = urllib.urlencode(data)
	page = urllib2.urlopen(url=url, data=dataEncode)
	return page.read()

def parsepage(page):
	soup = BeautifulSoup(page, 'html.parser')
	tables = soup.find_all("table", class_="wfresult")#tables 违章记录数组
	datas = []
	for table in tables:
		
		line1 = table.find('tr')
		line2 = line1.next_sibling.next_sibling
		line3 = line2.next_sibling.next_sibling
		line4 = line3.next_sibling.next_sibling
		line5 = line4.next_sibling.next_sibling
		#from line2
		hpzl = line2.find('td').next_sibling
		hphm = hpzl.next_sibling.next_sibling.next_sibling
		wfrq = hphm.next_sibling.next_sibling.next_sibling
		#from line3
		wfsj = line3.find('td').next_sibling
		cfzt = wfsj.next_sibling.next_sibling.next_sibling
		fkje = cfzt.next_sibling.next_sibling.next_sibling
		#from line4
		wfxw = line4.find('td').next_sibling
		#from line5
		wfdd = line5.find('td').next_sibling
		ykjf = wfdd.next_sibling.next_sibling.next_sibling
		
		"""
		trs = table.find_all("tr")
		for tr in trs:
			tds =  tr.children
			#print u'子节点的个数',len(tds)
			for td in tds:
				if not isinstance(td, bs4.element.NavigableString):#判断类型是否为字符串
					print td
		print
		print '1',hpzl.string
		print '2',hphm.string
		print '3',wfrq.string
		print '4',wfsj.string
		print '5',cfzt.string
		print '6',fkje.string
		print '7',wfxw.string
		print '8',wfdd.string
		print '9',ykjf.string
		"""
		data = {'hpzl':hpzl.string, 'hphm':hphm.string, 'wfrq':wfrq.string, 'wfsj':wfsj.string,\
		'cfzt':cfzt.string, 'fkje':fkje.string, 'wfxw':wfxw.string, 'wfdd':wfdd.string, 'ykjf':ykjf.string}
		datas.append(data)
	print datas


if __name__ == "__main__":
	parsepage(getpage()) 