from bs4 import BeautifulSoup
import urllib3
import re
import scraper
from Model import graph, models
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

test_spider = scraper.scraper()
#test_spider.manual_add("https://en.wikipedia.org/wiki/Tom_Hiddleston")
test_spider.start()
test_spider.complete_all()
test_spider.g.write_to_json('./')

print(test_spider.g.movie_num)
print(test_spider.g.actor_num)