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
	def __init__(self, link, folder, filename):
		threading.Thread.__init__(self)
		self.link = link
		self.folder = folder
		self.filename = filename
		return

	def downdown(self, link, folder, filename):
		link = link+folder+'/'+filename
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
		cookies = {'xa':'xa'}
		print 'start downloading ;...'+link
		print
		downreq = requests.get(link, headers = headers,\
		 cookies = cookies, hooks=dict(response=print_url))
		print 'download completed'+link
		print
		fullname = os.path.join(folder, filename+'.mp4')
		with open(fullname, 'wb') as downfile:
			downfile.write(downreq.content)
			downfile.close()

	def run(self):
		self.downdown(self.link, self.folder, self.filename)


def fuck():
	link = 'http://9.syasn.com/'
	folder = 'p'
	filename = 'p%d'
	start = 1
	end = 650
	count = 10
	progress = start

	downloaders = []

	#folder
	if not os.path.isdir(folder):
		os.mkdir(folder)
	
	#init
	for i in range(start, start + count):
		downloader = Downloader(link, folder, filename%progress)
		progress = progress + 1
		downloader.start()
		downloaders.append(downloader)

	while progress <= end:
		for downloader in downloaders:
			if not downloader.isAlive():
				downloaders.remove(downloader)
				downloader = Downloader(link, folder, filename%progress)
				progress = progress + 1
				downloader.start()
				downloaders.append(downloader)


if __name__ == "__main__":

	fuck()

	



