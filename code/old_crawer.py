#!/usr/bin/python
#-*-coding: utf-8 -*-

import requests
import queue
import re
from urllib.parse import urljoin , urlparse
from bs4 import BeautifulSoup

def headDepartment(title,soup):
	matchDomainThai = re.match( r'.*หัวหน้าภาควิชา.*', title, re.M|re.I) # check domain in xxx.ku.ac.th
	matchDomainEng = re.match( r'.*Department.Heads.*', title, re.M|re.I) # check domain in xxx.ku.ac.th
	if matchDomainThai or matchDomainEng:
		desc = soup.findAll(attrs={"name":"description"}) 
		print (desc[0]['content'])
		return True 

if __name__ == "__main__":
	dict = {} # store { "title":link , "title":link , ...}
	link_visited = [] # store visited links
	list_title = [] # store visited titles
	queue = queue.LifoQueue()
	seed_link = 'https://www.cpe.ku.ac.th/?lang=en' 
	step_number = 1 
	STEP_MAX = 1000
	QUEUE_MAX = 1000
	queue.put(seed_link) # put the first link
	while not queue.empty() :
		if step_number > STEP_MAX :
			break
		try :
			link = queue.get() # get a url link from q
			if  link not in link_visited :
				matchDomain = re.match( r'.*.ku.ac.th.*', link, re.M|re.I) # check domain in xxx.ku.ac.th
				if matchDomain: # domain in KU
					page = requests.get(link,timeout = 3, verify=False) # download page
					soup = BeautifulSoup(page.text)
					title = soup.title.string
					if title not in list_title :
						dict[title] = link # dict = {'url':'title' , ...}
						print ("%d.) %s : %s "%(step_number,title,link))
						is_found = headDepartment(title,soup)
						if is_found :
							print ("FOUND AT : %s"%link)
							break
						for x in soup.find_all('a'): # find all links
							fullpath = urljoin(link,x.get('href')) # get fullpath url
							if (queue.qsize()< QUEUE_MAX):
								queue.put(fullpath) # add all links into q
							# print (soup.title.string)
							# print (urljoin(link,x.get('href')))
						step_number+=1 # count steps
						link_visited.append(link)
						list_title.append(title)
		except (OSError, ValueError , AttributeError , NotImplementedError ,requests.exceptions.SSLError ) :
			print (">>> skip an error url : %s <<< "%(link))
	
# https://www.cpe.ku.ac.th/?page_id=1812&lang=en

	
	