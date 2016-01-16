# -*- coding:utf-8 -*- 

import requests
import bs4
from bs4 import BeautifulSoup
import os.path

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


def fuck(pageno):
	print 'fucking page %d'%pageno,'--------------'
	r = requests.get(url%pageno, proxies=proxies, verify=False)
	r.encoding = 'utf-8'
	soup = BeautifulSoup(r.text, 'html.parser')
	autopagerize_page_element = soup.find('div', class_='autopagerize_page_element')
	#posts = autopagerize_page_element.find_all('div', class_="post")
	#some tags are class="post xxx" so fuck those
	fuckposts = autopagerize_page_element.children
	posts = []
	for fuckpost in fuckposts:
		if isinstance(fuckpost, bs4.element.Tag):
			posts.append(fuckpost)
	count = 0
	for post in posts:
		count = count+1
		print 'post %d'%count
		#two types of photo shows
		photoposts = post.find('div', class_='photo-posts')
		media = photoposts.find('div', class_='media')
		photosets = photoposts.find('div', class_='photo-sets')
		if media != None:
			print '############media'
			img = media.find('img')['src']
			name = media.find('img')['alt'].strip().replace(':', '')+'.jpg'
			#name = media.find('div', class_='photoCaption').find('p').string.strip() anather method to get photo name
			print img,'    ',name
			downloadimg(img, name, imgpath)
		elif photosets != None:
			print '############photosets'
			#photosetgrid = photosets.find('div', class_='photoset-grid')
			imgs = photosets.find_all('img')
			if len(imgs) > 0:
				#get img name
				#fuck </br> , have to like this
				nametag = photosets.find('p')
				basename = nametag.contents[0].strip().replace(':', '')
				#basename = photosets.find('p').string.strip()
				imgindex = 1
				for img in imgs:
					img = img['src']
					name = basename+'_%d'%imgindex+'.jpg'
					print img,'    ',name
					downloadimg(img, name, imgpath)
					imgindex = imgindex + 1
		print '---------------------------------------'


if __name__ == '__main__':
	for i in range(13, 100):
		fuck(i)
	#caonimaurl = 'http://36.media.tumblr.com/2bbbda568cb211521ade5337ffea2ba7/tumblr_nxznw2OnXM1r2xjmjo1_1280.jpg'
	#filename = 'caonima'
	#downloadimg(caonimaurl, filename, imgpath)
	
