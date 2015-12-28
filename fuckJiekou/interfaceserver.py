import urllib
import urllib2
from bs4 import BeautifulSoup
import json
import tornado.ioloop
import tornado.web
"""
if __name__ == "__main__":
	userid = 669
	page = getpage(userid)
	jsondata = parsepage(page)
	print jsondata
"""
class ShuiFeiHandler(tornado.web.RequestHandler):
	def getpage(self, id):
		url = 'http://www.zzsgs.com/sfcx/'
		data = {'num':id}
		dataEncode = urllib.urlencode(data)
		page = urllib2.urlopen(url=url, data=dataEncode)
		return page.read()

	def parsepage(self, page):
		soup = BeautifulSoup(page, 'html.parser')
		table = soup.find("table", class_="m_search_list")

		datas = []
		for tr in table.find_all('tr'):
			id = tr.find('th')
			name = id.next_sibling
			address = name.next_sibling
			date = address.next_sibling
			quantity = date.next_sibling
			totalmoney = quantity.next_sibling
			remainmoney = totalmoney.next_sibling

			data = {'id':id.string, 'name':name.string, 'address':address.string,\
				'date':date.string, 'quantity':quantity.string, 'totalmoney':totalmoney.string, 'remainmoney':remainmoney.string}
			datas.append(data)
			
		jsondata = json.dumps(datas)
		return jsondata

	def get(self, userid):
		page = self.getpage(userid)
		jsondata = self.parsepage(page)
		self.write(jsondata)


class JiaoJingHandler(tornado.web.RequestHandler):

	
	def getpage(self, hpzl, hphm, clsbdh):
		url = 'http://218.59.228.162/wscgsxxcx/jdcwfcx.do'
		data = {'hpzl':hpzl, 'fzjg':'d', 'hphm':hphm, 'clsbdh':clsbdh, 'type':'wfcx'}
		dataEncode = urllib.urlencode(data)
		page = urllib2.urlopen(url=url, data=dataEncode)
		return page.read()

	def parsepage(self, page):
		soup = BeautifulSoup(page, 'html.parser')
		tables = soup.find_all("table", class_="wfresult")#tables 
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

			data = {'hpzl':hpzl.string, 'hphm':hphm.string, 'wfrq':wfrq.string, 'wfsj':wfsj.string,\
			'cfzt':cfzt.string, 'fkje':fkje.string, 'wfxw':wfxw.string, 'wfdd':wfdd.string, 'ykjf':ykjf.string}
			datas.append(data)
		
		jsondata = json.dumps(datas)
		return jsondata
	
	def get(self, hpzl, hphm, clsbdm):
		page = self.getpage(hpzl, hphm, clsbdm)
		jsondata = self.parsepage(page)
		self.write(jsondata)

application = tornado.web.Application([
    (r"/shuifei/userid/\d+", ShuiFeiHandler),    
    (r"/jiaojing/hpzl/(\d+)/hphm/(\w{5})/clsbdm/(\d{6})", JiaoJingHandler),    
])



if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    


