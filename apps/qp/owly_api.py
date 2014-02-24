import json
import urllib2

OWLY_API_KEY = "XUjFVNXjMU0cdDDWPctxq"
BASE_URL = "http://ow.ly/api/1.1/"

# see http://ow.ly/api-docs
# we will support 3 methods: /url/shorten/ , /url/expand/ , /url/info/ , and /url/clickStats

class Owly:
	def url_shorten(self,longUrl):
		url = BASE_URL+"url/shorten?apiKey="+OWLY_API_KEY+"&longUrl="+longUrl
		return json.load(urllib2.urlopen(url))

	def test_url_shorten(self):
		shorten_response = self.url_shorten("http://twitter.com")
		print shorten_response['results']
		print shorten_response['results']['shortUrl']
		shorten_response_2 = self.url_shorten("http://quidprize.com/stbks_abtsfrd/1234")
		print shorten_response_2['results']

	def url_expand(self,shortUrl):
		url = BASE_URL+"url/expand?apiKey="+OWLY_API_KEY+"&shortUrl="+shortUrl
		return json.load(urllib2.urlopen(url))

	def test_url_expand(self):
		expand_response = self.url_expand("http://ow.ly/2atOd8")
		print expand_response['results']
		print expand_response['results']['longUrl']

	def url_info(self,shortUrl):
		url = BASE_URL+"url/info?apiKey="+OWLY_API_KEY+"&shortUrl="+shortUrl
	        return json.load(urllib2.urlopen(url))

	def test_url_info(self):
		info_response = self.url_info("http://ow.ly/2atNcB")
		print info_response['results']

	def url_clickStats(self,shortUrl,fr='',to=''):
		url = BASE_URL+"url/clickStats?apiKey="+OWLY_API_KEY+"&shortUrl="+shortUrl
		if fr!='':
			url += "&from="+fr
		if to!='':
			url += "&to="+to
	        return json.load(urllib2.urlopen(url))

	def test_url_clickStats(self):
		clickstats_response = self.url_clickStats("http://ow.ly/1234")
		print clickstats_response['results']


