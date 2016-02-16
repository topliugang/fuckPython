# -*- coding:utf-8 -*- 

import requests
import bs4
from bs4 import BeautifulSoup
import os.path
import json

url = 'http://wanimal1983.tumblr.com/page/%d'

proxies = {
        'http': 'http://127.0.0.1:8087',
        'https': 'http://127.0.0.1:8087',
}

imgpath = '.\\wanimal'


def downloadimg(url, filename, path):
	print 'downloading img ',filename
	r = requests.get(url, proxies=proxies, stream=True, timeout=300)
	fullpath = os.path.join(path, filename)
	with open(fullpath, 'wb') as imgfile:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				imgfile.write(chunk)
				imgfile.flush()
		imgfile.close()
	return fullpath


def nomercy(pageid):
	"""
	简直无情api：
	authKey : awrXoqWrcg2qeK3kbfohdSFIysTYoxa5CGBpEehwb9MxxNVGg7
	http://api.tumblr.com/v2/blog/wanimal1983.tumblr.com/posts?api_key=awrXoqWrcg2qeK3kbfohdSFIysTYoxa5CGBpEehwb9MxxNVGg7&limit=15&offset=15
	"""
	url = 'http://api.tumblr.com/v2/blog/wanimal1983.tumblr.com/posts?api_key=awrXoqWrcg2qeK3kbfohdSFIysTYoxa5CGBpEehwb9MxxNVGg7&limit=15&offset=15'
	r =requests.get(url=url, proxies=proxies, verify=False)
	r.encoding = 'utf-8'
	
	s = json.loads(r.text)
	postlist = s['response']['posts']
	for post in postlist:
		print post['post_url']
		postsummary = post['summary']
		photolist = post['photos']
		i = 0
		for photo in photolist:
			photourl = photo['original_size']['url']
			print photourl
			downloadimg(photourl, postsummary+'%d.jpg'%i, imgpath)
			i = i+1
		print 




if __name__ == '__main__':
	for i in range()
	

	
