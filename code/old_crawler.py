#!/usr/bin/python
#-*-coding: utf-8 -*-

import requests
import queue
import re
from urllib.parse import urljoin
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import sys
import time
from urllib import robotparser

def downloadPage(number,page,url):
	file_name = str(number)+".html"
	file = open(file_name, "w")
	file.write(page.text)
	file.write("<url>"+ url +"</url>")
	file.close()

def addRelations(fromSource,url,filename):
	rel = "%s,%s\n"%(fromSource[url],url)
	filename.write(rel)
		
def detectLoadingErrorPage(url,page,filename):
	http_status_code = page.status_code
	if http_status_code >= 400  and http_status_code < 600 :
		err = "%s -> status code : %d , description : %s\n"%(url,http_status_code,requests.status_codes._codes[http_status_code][0])
		filename.write(err)

def detectCourse(url,soup,filename):
	url_course = re.match( r'.*http://www.eng.ku.ac.th/.page_id=9690$', url, re.M|re.I) # check domain in xxx.ku.ac.th
	if url_course:
		desc = soup.findAll(attrs={"class":"wonderplugintabs-panel-inner"}) 
		filename.write(desc[0].get_text()[0:620]+"\n")

def robotsChecker(fullpath):
	try:
		hostname = urlparse(fullpath).scheme+"://"+urlparse(fullpath).hostname+"/robots.txt"
		rp = robotparser.RobotFileParser()
		rp.set_url(hostname)
		rp.read()
		return rp.can_fetch("SUPERMAN CPE27\'s BOT", fullpath)
	except :
		print ("error : \"%s\" "%fullpath)
		return True
	

if __name__ == "__main__":
	
	queue = queue.Queue() # .LifoQueue()
	step_number = 1 
	STEP_MAX = 1000
	QUEUE_MAX = 1000

	filename_relation_urls = open("relation_urls.txt", "w")
	# filename_detect_loading_error_page = open("detect_loading_error_page.txt", "w")
	# filename_detect_couse_eng = open("detect_couse_eng.txt", "w")

	fromSource = {}
	task_queue = []
	seed_link = 'https://mike.cpe.ku.ac.th/seed/'
	fromSource[seed_link] = "null(start)"
	queue.put(seed_link) # put the first url

	while not queue.empty() :
		if step_number > STEP_MAX :
			break
		try :
			url = queue.get()
			if robotsChecker(url) : # robots.txt
				page = requests.get(url,timeout = 5, verify=False ,headers={'User-Agent':'SUPERMAN CPE27\'s BOT'}) 
				soup = BeautifulSoup(page.text)
				
				# detectCourse(url,soup,filename_detect_couse_eng)
				# detectLoadingErrorPage(url,page,filename_detect_loading_error_page)
				addRelations(fromSource,url,filename_relation_urls)
				# downloadPage(step_number,page,url)
					
				for x in soup.find_all('a'): # find all links
					fullpath = urljoin(url,x.get('href')) # get fullpath url
					if queue.qsize() < QUEUE_MAX and fullpath not in task_queue:
						matchDomain = re.match( r'.*.ku.ac.th.*', fullpath, re.M|re.I)
						extension = re.compile('.*\.(jpg|png|pdf|ppt|rar|zip|gif|doc|docx|mp4|xls|docx|doc)') 
						if matchDomain and not extension.match(fullpath):
							fromSource[fullpath] = url
							queue.put(fullpath)
							task_queue.append(fullpath)
				step_number+=1 # count steps
				sys.stdout.write("Download progress: %d%%   (%d:%d)\r" % (step_number/STEP_MAX*100,step_number-1,STEP_MAX) )
				sys.stdout.flush()
				time.sleep(1)
			else :
				print ("Disallow : %s"%url)
		except (OSError, ValueError , TypeError , NotImplementedError ,AttributeError,requests.exceptions.SSLError ,requests.exceptions.ConnectionError) : #OSError, ValueError , TypeError , NotImplementedError ,AttributeError,requests.exceptions.SSLError ,requests.exceptions.ConnectionError
			QUEUE_MAX+=1
			
	filename_relation_urls.close()
	filename_detect_loading_error_page.close()
	filename_detect_couse_eng.close()
	print ("Download Completed")


	
	