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


def robotsChecker(fullpath):
	hostname = urlparse(fullpath).scheme+"://"+urlparse(fullpath).hostname+"/robots.txt"
	print (hostname)
	rp = robotparser.RobotFileParser()
	rp.set_url(hostname)
	rp.read()
	return rp.can_fetch("NAT's BOT", fullpath)

def dictQueue():
	dictQueue = {}
	x = "a"
	dictQueue[x] = queue.Queue()
	dictQueue[x].put("1")
	return dictQueue[x].get()

if __name__ == "__main__":
	# print (robotsChecker("http://mike.cpe.ku.ac.th/asdasdasds"))
	print (dictQueue())
	


	
	