# Python 3

from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse

class WebsiteValidator(object):
	# Class constructor
	def __init__(self, starting_url):
		self.starting_url = starting_url
		self.domain = urlparse(self.starting_url).netloc
		self.visited = set()
		self.print_info = []
		self.driver = webdriver.Firefox()
		
	# Crawl through links
	def crawl(self, url):
		if (url.endswith("/")):
			url = url[:-1]
		self.driver.get(url)
		print(url)
		self.visited.add(url)
		# do something
		for link in self.get_links(url):
			if link in self.visited:
				continue
			self.crawl(link)
	
	# Get links as a set
	def get_links(self, url):
		links_tags = ["a", "link", "script"]
		links_to_see = set()
		for link_tag in links_tags:
			link_elements = self.driver.find_elements_by_tag_name(link_tag)
			for link_element in link_elements:
				if ((link_tag == "a") or (link_tag == "link")):
					link = link_element.get_attribute("href")
				else:
					link = link_element.get_attribute("src")
				if ((link is None) or (link is "")):
					self.print_info.append("No HREF/SRC: " + link_element.get_attribute("class"))
				else:
					if ((self.domain not in link) or (link.startswith("mailto:")) or (link.startswith("tel:"))):
						self.print_info.append("SKIPPED: " + link)
					else:
						if link not in self.visited:
							links_to_see.add(link)
		return links_to_see
	
	# Begin crawling and close WebDriver when finished
	def start(self):
		self.crawl(self.starting_url)
		self.driver.close()

if __name__ == "__main__":
	starting_url = "https://google.com/"
	validator = WebsiteValidator(starting_url)
	validator.start()
