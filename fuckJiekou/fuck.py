# -*- coding:utf-8 -*- 
import requests
from bs4 import BeautifulSoup

url = 'http://javpop.com/category/censored'
pageurl = 'http://javpop.com/2015/12/28/tek-071.html'
filename = 'javapop.html'

proxies = {
        'http': 'http://127.0.0.1:8087',
        'https': 'http://127.0.0.1:8087',
}


r = requests.get(pageurl, proxies=proxies, verify=False)
pagefile = open(filename, 'w')
#pagefile.write(r.text.decode('iso-8859-1').encode('utf8'))
text = r.text
print text
#text.decode('')
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