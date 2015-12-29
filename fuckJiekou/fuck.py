# -*- coding:utf-8 -*- 
import requests
from bs4 import BeautifulSoup

urlout = 'https://www.youtube.com/'
urlout1 = 'https://www.tumblr.com/'
urlin = 'https://www.zhihu.com/'
urlfuck = 'http://iour.co/category/jav-uncensored/'
urlfuckpage = 'http://iour.co/category/jav-uncensored/page/'
proxies = {
        'http': 'http://127.0.0.1:8087',
        'https': 'http://127.0.0.1:8087',
}

"""
r = requests.get(urlfuck, proxies=proxies, verify=False)
pagefile = open('iour.html', 'w')
pagefile.write(r.text)
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
	r = requests.get(urlfuckpage+'%d'%i, proxies=proxies, verify=False)
	pagefile = open('iour.html%d'%i, 'w')
	pagefile.write(r.text)





"""


"""
