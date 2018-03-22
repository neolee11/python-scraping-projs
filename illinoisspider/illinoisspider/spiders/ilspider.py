
import scrapy
from scrapy import Request
from bs4 import BeautifulSoup


class ilspider(scrapy.Spider):
	name = "ilspider"

	def start_requests(self):
		url = 'http://www.dfr.vermont.gov/reg-bul-ord/vermont-securities-regulations'
		yield scrapy.Request(url=url, callback=self.parse)


	def parse(self, response):
		html_doc = BeautifulSoup(response.body, "lxml")
		filename = 'result.html'
		with open(filename, 'wb') as f:
			f.write(response.body)
		print(html_doc)
