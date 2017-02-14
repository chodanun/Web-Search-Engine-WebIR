import networkx as nx
from bs4 import BeautifulSoup

D=nx.DiGraph()
relation = open("/Users/chodanunsrinil/Desktop/CPE#4/lucune/code/relation_urls.txt").read()
relation = relation.split('\n')

for i in relation:
	pair = i.split(',')
	try:
		D.add_edge(pair[0],pair[1])
	except (IndexError,KeyError):
		pass
	

pagerank = nx.pagerank(D,0.85)

# for i in relation:
# 	pair = i.split(',')
# 	print (pagerank[pair[0]])


for i in range(1,1001):
	file_name = "/Users/chodanunsrinil/Desktop/CPE#4/lucune/data/"+str(i)+".html"
	file = open(file_name,"r").read()
	soup = BeautifulSoup(file, "html.parser")
	try:
		url = soup.url.string
		score = pagerank[url]
	except (KeyError,AttributeError):
		score = 0
		print ("error : "+str(i))
	
	file_new = open(file_name,"w")
	file_new.write(file)
	file_new.write("<pagerank>"+str(score)+"</pagerank>")
	print (i)
	
# D.add_edge("null(start)","https://mike.cpe.ku.ac.th/seed/")
# D.add_edge("https://mike.cpe.ku.ac.th/seed/","http://www.eng.ku.ac.th/")

# file = open("/Users/chodanunsrinil/Desktop/CPE#4/lucune/data/1.html","r").read()
# file_new = open("/Users/chodanunsrinil/Desktop/CPE#4/lucune/data/1.html","w")
# file_new.write(file)
# file_new.write("10test10")
# print (nx.pagerank(D,0.85))