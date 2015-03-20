import urllib2
from urllib2 import urlopen
import cookielib
from cookielib import CookieJar
import re
import time

cj = CookieJar() # Not absolutely necessary but recommended
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')] # To be able to crawl on websites that blocks Robots

def readSourceCode():
	try:
		page = 'http://logs.nodejs.org/node.js/index'
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

def pullLinks(sourceCode, exclude=None, include=None):
	regex = '<a href="(.*?)">'
	print exclude
	return pullItems(sourceCode=sourceCode, exclude=exclude, include=include, regex=regex)

def main():
	sourceCode = readSourceCode()
	links = pullLinks(sourceCode=sourceCode)
	for link in links:
		print link

if __name__ == '__main__':
	main()