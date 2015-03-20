#Crawls and extracts data from a webpage
from urllib import urlopen 
from bs4 import BeautifulSoup
import mechanize
import re

#returns text stripped from of the HTML website
def crawl(url):
	print ("Crawling...")
	webpage = url
	br = mechanize.Browser()
	data = br.open(webpage).get_data()
	soup = BeautifulSoup(data)
	soup.prettify()
	#print soup
	return soup

def scrapPosts(soup, MAX=None):
	print ("Mining Posts...")
	text = (soup.get_text()).encode('utf-8').split('\n')
	data = []
	for line in text:
		if '<' in line:
			temp = re.split('[<>]', line)
			nick = temp[1]
			post = temp[2]
			timestamp = post[-10:]
			comment = post[:-10]
			data.append(nick+"===="+comment+"-----"+timestamp)
	if MAX is None:
		return data
	else:
		return data[:MAX]

def scrapURLs(soup, MAX=None):
	print ("Mining URLs...")
	text1 = soup.findAll('a', href=True)
	#text = (soup.get_text()).encode('utf-8').split('\n')
	urls = []
	for line in text1:
		if 'latest' not in line:
			datestamp = line.get_text()
			urls.append(['http://logs.nodejs.org/node.js/'+datestamp, datestamp])
	if MAX is None:
		return urls
	else:
		return urls[:MAX]


def main():
    soup =  crawl('http://logs.nodejs.org/node.js/index')
    #data = scrapPosts(soup)
    data = scrapURLs(soup, 5)

    soup1 = crawl(data[1][0])
    data1 = scrapPosts(soup1, MAX=5)
    #print data
    print "DATA FOR: "+data[1][1]
    for x in data1:
    	print(x)
    #	pass


if __name__ == '__main__':
    main()

exit(0)
#print soup