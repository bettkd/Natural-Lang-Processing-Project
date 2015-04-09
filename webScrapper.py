import urllib2
from urllib2 import urlopen
import cookielib
from cookielib import CookieJar
import re
import time
import json

cj = CookieJar() # Not absolutely necessary but recommended
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')] # To be able to crawl on websites that blocks Robots

def readSourceCode(page):
	try:
		sourceCode = opener.open(page).read()
		return sourceCode
	except Exception, e:
		print str(e)

def pullItems(sourceCode, exclude=None, include=None, regex=""): # Exclude request overrides include
	try:
		items = re.findall(r'%s'%regex, sourceCode)

		print items
		if exclude:
			x_items = []
			for item in items:
				if item not in exclude:
					x_items.append(item)
			return x_items
		elif include:
			i_items = []
			for item in items:
				if item in include:
					i_items.append(item)
			return i_items
		else:
			return items
	except Exception, e:
		print str(e)

#def pullContent(sourceCode):
#	try:
#		text = re.findall(r'<td class="nick">(.*?)</td>.*?"content">(.*?)</td>.*?name="(.*?)"', sourceCode)
#		return text
#	except Exception, e:
#		print str(e)

def readJson(jFile):
	with open(jFile, "r") as data_file:
		config = json.load(data_file)
	data_file.close()
	return config

def writeJson(jFile, data):
	with open(jFile, 'w') as outfile:
		json.dump(data, outfile, indent=4)
	outfile.close()

def execute():
	#readConfig
	config = readJson(jFile='scrapper_config.json')
	#readPage
	page = config["page"]
	sourceCode = readSourceCode(page=page).encode('utf-8')
	#pullLinks
	pullLinks = config["pullLinks"]
	regex = pullLinks['regex']
	exclude = pullLinks['exclude']
	links = pullItems(sourceCode=sourceCode, regex=regex, exclude=exclude)
	dataLinks = {"links":["http://logs.nodejs.org/node.js/"+l for l in links]}
	writeJson(jFile='dataLinks.txt', data=dataLinks)
	#pullContent
	pullCont = config["pullContent"]
	regex1 = pullCont["regex"]
	include1 = pullCont["include"]
	content = dict()
	#print dataLinks["links"]
	for page1 in dataLinks["links"]:
		sourceCode1 = readSourceCode(page=page1)
		(user, cont, timStamp) = pullItems(sourceCode=sourceCode1, regex=regex1, include=include1)
		#print cont
		#content[page1] = {"user":user, "content":cont, "timeStamp":timeStamp}

	#print content




def main():
	#page = 'http://logs.nodejs.org/node.js/index'
	#sourceCode = readSourceCode(page=page)

	#data1 = {"page":"url", "pull":{"include":"None", "exclude":"None", "regex":"ndnd"}}
	#with open('scrapper_config.json', 'w') as outfile:
	#	json.dump(data1, outfile, indent=4)


	execute()

	
	
	#for link in links:
	#	print link

	#sourceCode = readSourceCode("http://logs.nodejs.org/node.js/2012-04-06")
	
	
	#user = pullContent(sourceCode)
	#for x in pullItems(sourceCode, regex=regex):
	#	user, cont, tim = x
	#	print cont
	#print user
	#for item in items:
	#	print item
	#for x in  pullContent(sourceCode):
	#	print x

if __name__ == '__main__':
	main()