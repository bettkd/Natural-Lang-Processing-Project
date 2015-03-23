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
		links = re.findall(r'%s'%regex, sourceCode)
		if exclude:
			xlinks = []
			for link in links:
				if link not in exclude:
					xlinks.append(link)
			return xlinks
		elif include:
			ilinks = []
			for link in links:
				if link in include:
					ilinks.append(link)
			return ilinks
		else:
			return links
	except Exception, e:
		print str(e)

def pullContent(sourceCode):
	try:
		text = re.findall(r'<td class="nick">&lt;(.*?)&gt;</td><td class="content">(.*?)</td>', sourceCode)
		return text
	except Exception, e:
		raise e

def main():
	#page = 'http://logs.nodejs.org/node.js/index'
	#sourceCode = readSourceCode(page=page)

	#data1 = {"page":"url", "pull":{"include":"None", "exclude":"None", "regex":"ndnd"}}
	#with open('scrapper_config.json', 'w') as outfile:
	#	json.dump(data1, outfile, indent=4)


	with open('scrapper_config.json', "r") as data_file:
		config = json.load(data_file)
	data_file.close()

	page = config["page"]
	pullLinks = config["pullLinks"]
	regex = pullLinks['regex']
	exclude = pullLinks['exclude']

	sourceCode = readSourceCode(page=page).encode('utf-8')
	links = pullItems(sourceCode=sourceCode, regex=regex, exclude=exclude)

	dataLinks = {"links":["http://logs.nodejs.org/node.js/"+l for l in links]}
	with open('dataLinks.txt', 'w') as outfile:
		json.dump(dataLinks, outfile, indent=4)
	outfile.close()
	
	#for link in links:
	#	print link

	sourceCode = readSourceCode("http://logs.nodejs.org/node.js/2012-04-06")
	print pullContent(sourceCode)

if __name__ == '__main__':
	main()