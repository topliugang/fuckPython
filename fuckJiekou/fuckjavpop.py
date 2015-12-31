# -*- coding:utf-8 -*- 
import requests
from bs4 import BeautifulSoup


pageurl = 'http://javpop.com/2015/12/30/mmr-ap004_marika_kuroki.html'


proxies = {
        'http': 'http://127.0.0.1:8087',
        'https': 'http://127.0.0.1:8087',
}

#globals
censoredurl = 'http://javpop.com/category/censored/'#url
censoredpageurl = 'http://javpop.com/category/censored/page/%d'
censoredpage = ''
censoredsoup = None
maxpage = 0

def initcensored():
	r = requests.get(censoredurl, proxies=proxies, verify=False)
	r.encoding = 'utf-8'#默认是 ISO-8859-1
	global censoredpage
	global censoredsoup
	global maxpage
	censoredpage = r.text
	censoredsoup = BeautifulSoup(censoredpage, 'html.parser')
	lasttag = censoredsoup.find('a', class_='last')
	maxpage = int(lasttag['href'].split('/')[-1])#取最后一个

def getpostlinks(pageurl):
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
	r = requests.get(posturl, proxies=proxies, verify=False)
	r.encoding = 'utf-8'#默认是 ISO-8859-1
	page = r.text
	soup = BeautifulSoup(page, 'html.parser')
	print page


if __name__ == '__main__':
	initcensored()
	#for i in range(maxpage+1):
		#for j in getpostlinks(censoredpageurl%i):
		#	print j
	#	pageurl = censoredpageurl%i
	pageurl = censoredpageurl%444
	posturls = getpostlinks(pageurl)
	posturl = posturls[3]
	fuckpost(posturl)



	

    
    

"""
pagefile = open('iour.html', 'r')
page = pagefile.read()
soup = BeautifulSoup(page, 'html.parser')
divs = soup.find_all('div', class_='thumb-img')
for div in divs:
	#print div
	a = div.find('a')
	title = a['title']
	pagelink = a['href']
	img = a.find('img')
	imglink = img['src']

	#print title
	#print pagelink
	#print imglink
	#print 

last = soup.find('a', class_='last')
maxpage = last['href'].split('/')[-1]#取最后一个
maxpage = int(maxpage)


for i in range(maxpage+1):
	r = requests.get(urliourpage+'%d'%i, proxies=proxies, verify=False)
	pagefile = open('iour.html%d'%i, 'w')
	pagefile.write(r.text)



"""