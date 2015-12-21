 # -*- coding:utf-8 -*- 
import requests
from bs4 import BeautifulSoup
import threading
import os


"""
解析页面到各种url
url = 'http://9.syasn.com/9v/9v108'
url2 = 'http://www.flv.tv/9v109'
fuckurl = 'http://www.flv.tv/9v106'
fuckurl2 = 'http://www.flv.tv/9v88'

down1 = 'http://1.syasn.com/'
down2 = 'http://k.syasn.com/'
down3 = 'http://11.syasn.com/'
down4 = 'http://n.syasn.com/'
down5 = 'http://9.syasn.com/'

req = requests.get(fuckurl2)
page = req.text
soup = BeautifulSoup(page, 'html.parser')
tag = soup.find('a', id='n1')
print tag
folder = tag['type']
file = tag['href']
downlink = down5+folder+'/'+file
"""

def print_url(r, *args, **kwargs):
    #print(r.content)
    print r.is_redirect


"""
link = 'http://9.syasn.com/'
folder = '3v'
filename = '3v%d'

"""



"""
multithreading instance
"""
class Downloader(threading.Thread):
	def __init__(self, link, path, folder, filename):
		threading.Thread.__init__(self)
		self.link = link
		self.path = path
		self.folder = folder
		self.filename = filename
		return

	def downdown(self, link, path, folder, filename):
		link = link+folder+'/'+filename
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
		cookies = {'xa':'xa'}
		print 'start downloading ;...'+link
		print
		downreq = requests.get(link, headers = headers,\
		 cookies = cookies, hooks=dict(response=print_url))
		print 'download completed'+link
		print
		fullname = os.path.join(path, folder, filename+'.mp4')
		with open(fullname, 'wb') as downfile:
			downfile.write(downreq.content)
			downfile.close()

	def run(self):
		self.downdown(self.link, self.path, self.folder, self.filename)


def fuck(link, folder, filename, start, end, count, path):
	
	progress = start

	downloaders = []

	#folder
	fullpath = os.path.join(path, folder)
	if not os.path.isdir(fullpath):
		os.mkdir(fullpath)
	
	#init
	for i in range(start, start + count):
		downloader = Downloader(link, path, folder, filename%progress)
		progress = progress + 1
		downloader.start()
		downloaders.append(downloader)

	while progress <= end:
		for downloader in downloaders:
			if not downloader.isAlive():
				downloaders.remove(downloader)
				downloader = Downloader(link, path, folder, filename%progress)
				progress = progress + 1
				downloader.start()
				downloaders.append(downloader)

#check from start to end
#like 1 -- 116
def checkanddown(link, start, end, path, folder, filename):
	for i in range(start, end+1):
		name = filename%i+'.mp4'
		fullpath = os.path.join(path, folder, name)
		if not os.path.exists(fullpath):
			print name, 'not exists'
			downloader = Downloader(link, path, folder, filename%i)
			downloader.start()

def check(link, start, end, path, folder, filename):
	for i in range(start, end+1):
		name = filename%i+'.mp4'
		fullpath = os.path.join(path, folder, name)
		if not os.path.exists(fullpath):
			print name, 'not exists'
			#downloader = Downloader(link, path, folder, filename%i)
			#downloader.start()








if __name__ == "__main__":

	link = 'http://9.syasn.com/'
	folder = '3v'
	filename = '3v%d'
	start = 1
	end = 31
	count = 10
	path = 'c:\\develop\\fuck'

	#fuck(link, folder, filename, start, end, count, path)
	checkanddown(link, start, end, path, folder, filename)
	#check(link, start, end, path, folder, filename)

	



