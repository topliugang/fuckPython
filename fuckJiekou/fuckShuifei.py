import urllib
import urllib2
from bs4 import BeautifulSoup
import json
import tornado.ioloop
import tornado.web



def getpage(id):
	url = 'http://www.zzsgs.com/sfcx/'
	data = {'num':id}
	dataEncode = urllib.urlencode(data)
	page = urllib2.urlopen(url=url, data=dataEncode)
	return page.read()

def parsepage(page):
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


"""
if __name__ == "__main__":
	userid = 669
	page = getpage(userid)
	jsondata = parsepage(page)
	print jsondata
"""
	
class FuckHandler(tornado.web.RequestHandler):
    def get(self, userid):
        #self.write("You requested the story " + userid)
        page = getpage(userid)
        jsondata = parsepage(page)
        self.write(jsondata)


application = tornado.web.Application([
    (r"/userid/([0-9]+)", FuckHandler),    
])



if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    print "started"


