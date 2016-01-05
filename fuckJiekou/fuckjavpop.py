# -*- coding:utf-8 -*- 
import requests
from bs4 import BeautifulSoup

proxies = {
        'http': 'http://127.0.0.1:8087',
        'https': 'http://127.0.0.1:8087',
}

categoris = [
	'idol',				#0
	'censored',			#1
	'uncensored',		#2
]

#globals
categoryurl = 'http://javpop.com/category/%s/'#url
categorypageurl = 'http://javpop.com/category/%s/page/%d'
imgsdir = '../imgs/'

def init(categorytype):
	r = requests.get(categoryurl%categoris[categorytype], proxies=proxies, verify=False)
	r.encoding = 'utf-8'#默认是 ISO-8859-1
	soup = BeautifulSoup(r.text, 'html.parser')
	lasttag = soup.find('a', class_='last')
	maxpage = int(lasttag['href'].split('/')[-1])#取最后一个
	return maxpage

def getpostlinks(pageurl):
	print 'getting post links from page url: ', pageurl
	r = requests.get(pageurl, proxies=proxies, verify=False)
	r.encoding = 'utf-8'#默认是 ISO-8859-1
	page = r.text
	soup = BeautifulSoup(page, 'html.parser')
	links = []
	ultag = soup.find('ul', class_='thumb_post')
	lis = ultag.find_all('li')
	for li in lis:
		a = li.find('a')
		links.append(a['href'])
	return links

def fuckpost(posturl):
	print 'fucking post from url: ', posturl
	r = requests.get(posturl, proxies=proxies, verify=False)
	r.encoding = 'utf-8'#默认是 ISO-8859-1
	page = r.text
	soup = BeautifulSoup(page, 'html.parser')
	postbox = soup.find('div', class_='post box')

	postid = postbox['id']
	title = postbox.find('h1').string
	poster = postbox.find('p', class_='poster')
	posterimgurl = poster.find('img')['src']
	screenshot = postbox.find('p', class_='screenshot')
	screenshotimgurl = screenshot.find('img')['src']

	postmeta = postbox.find('div', class_='post-meta-b')
	tags = []
	if postmeta is not None:
		tagtags = postmeta.find_all('a')
		for tag in tagtags:
			tags.append(tag.string)

	posterimgpath = downloadimg(posterimgurl)
	screenshotimgpath = downloadimg(screenshotimgurl)
	print 'postid:  ', postid ##useless
	print 'title:  ',title
	print 'posterimgurl:  ',posterimgurl
	print 'posterimgpath:  ',posterimgpath
	print 'screenshotimgurl:  ',screenshotimgurl
	print 'screenshotimgpath:  ',screenshotimgpath
	print 'tags:  ',
	for tag in tags:
		print tag,' ',

	return postid, title, posterimgurl, posterimgpath, screenshotimgurl, screenshotimgpath, tags
	
	
def downloadimg(url):
	filename = url.split('/')[-1]
	print 'downloading img ',filename
	r = requests.get(url, stream=True, timeout=10)
	with open(imgsdir+filename, 'wb') as imgfile:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				imgfile.write(chunk)
				imgfile.flush()
		imgfile.close()
	return imgsdir+filename

###########################################################################################################
import sqlite3

createtablefilename = 'createTable.sql'

dbfilename = 'fuck.db'

con = None

cur = None

categorisdb = [
	('idol',),				#0
	('censored',),			#1
	('uncensored',),		#2
]

def initdb():
	global con
	global cur
	con = sqlite3.connect(dbfilename)
	cur = con.cursor() 



def closedb():
	global con
	global cur
	cur.close()
	con.close()

def createtable():
	sqlFile = open(createtablefilename, 'r')
	sqls = sqlFile.read()
	cur.executescript(sqls)
	con.commit()

def insertcategory():
	cur.executemany("insert into category(name) values(?)", categorisdb)
	con.commit()

def insertimg(imgurl, imgpath):
	cur.execute("insert into img(url, filepath) values(?, ?)", (imgurl, imgpath))
	con.commit()
	return int(cur.lastrowid)
	
def insertpost(postid, title, categoryid, tags, posterimgurl, posterimgpath, screenshotimgurl, screenshotimgpath):
	print 'inserting...................................................................................'
	#insert imgs
	posterimgid = insertimg(posterimgurl, posterimgpath)
	screenshotimgid = insertimg(screenshotimgurl, screenshotimgpath)
	#insert post
	cur.execute("insert into post(postid, title, categoryid, posterimgid, screenshotimgid) values(?, ?, ?, ?, ?)",\
		(postid, title, categoryid, posterimgid, screenshotimgid) )
	con.commit()
	postid = int(cur.lastrowid)
	#inserttags
	inserttag(tags, postid)
	
def inserttag(tags, postid):
	for tag in tags:
		cur.execute("select id from tag where name = ?", (tag,))
		tagid = cur.fetchone()
		if tagid:
			cur.execute("insert into posttag(postid, tagid) values(?, ?)", (postid, tagid[0]))
			con.commit()
		else:#tagid is None
			cur.execute("insert into tag(name) values(?)", (tag,))
			con.commit()
			tagid = int(cur.lastrowid)
			cur.execute("insert into posttag(postid, tagid) values(?, ?)", (postid, tagid))
			con.commit()

def checkpost(postid):
	cur.execute("select id from post where postid = ?", (postid,))
	res = cur.fetchone()
	if res:
		return True
	else:
		return False

###########################################################################################################




def test():
	posturl = 'http://javpop.com/2016/01/02/muramura-010216_333.html'
	sb = fuckpost(posturl)	
	print len(sb)
	postid, title, posterimgurl, posterimgpath, screenshotimgurl, screenshotimgpath, tags = fuckpost(posturl)	
	insertpost(postid, title, categorytype, tags, posterimgurl, posterimgpath, screenshotimgurl, screenshotimgpath)
	
def resetdb():
	initdb()
	createtable()
	insertcategory()
	closedb()

def fuckc(categorytype):
	initdb()
	maxpage = init(categorytype)
	print 'maxpage is :', maxpage
	for i in range(1, maxpage+1):
		print 'fucking page: %d'%i
		for posturl in getpostlinks(categorypageurl%(categoris[categorytype], i)):
			postid, title, posterimgurl, posterimgpath, screenshotimgurl, screenshotimgpath, tags = fuckpost(posturl)
			if not checkpost(postid):
				insertpost(postid, title, categorytype, tags, posterimgurl, posterimgpath, screenshotimgurl, screenshotimgpath)
	closedb()

def fuckp(categorytype, pageid):
	initdb()
	maxpage = init(categorytype)
	if pageid > maxpage or pageid <= 0:
		print "page out of range"
		closedb()
		return False

	
	print 'fucking page:%d'%pageid
	for posturl in getpostlinks(categorypageurl%(categoris[categorytype], pageid)):
		postid, title, posterimgurl, posterimgpath, screenshotimgurl, screenshotimgpath, tags = fuckpost(posturl)
		if not checkpost(postid):
			insertpost(postid, title, categorytype, tags, posterimgurl, posterimgpath, screenshotimgurl, screenshotimgpath)
	closedb()

def fuckpp(categorytype, pageidstart, pageidend):
	initdb()
	maxpage = init(categorytype)
	if pageidstart > pageidend or pageidstart > maxpage or pageidend <= 0 :
		print "page out of range"
		closedb()
		return False

	
	print 'fucking page: start--%d, end--%d'%(pageidstart, pageidend)
	for i in range(pageidstart, pageidend+1):
		print 'fucking page: %d'%i
		for posturl in getpostlinks(categorypageurl%(categoris[categorytype], i)):
			postid, title, posterimgurl, posterimgpath, screenshotimgurl, screenshotimgpath, tags = fuckpost(posturl)
			if not checkpost(postid):
				insertpost(postid, title, categorytype, tags, posterimgurl, posterimgpath, screenshotimgurl, screenshotimgpath)
	closedb()	


if __name__ == '__main__':
	#resetdb()
	
	fuckpp(2, 12, 468)
	#test()
	
	#fuck(0, 2)
	#fuck(0, 222)
	#fuck(0, 2)
	#fuck(1)
	#fuck(2)
	