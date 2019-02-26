from bs4 import BeautifulSoup
import urllib3
import re
import scraper
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## https://stackoverflow.com/questions/36516183/what-should-i-use-to-open-a-url-instead-of-urlopen-in-urllib3


'''
wiki = "https://en.wikipedia.org/wiki/Haven_(film)"
http = urllib3.PoolManager()
response = http.request('GET', wiki)
soup = BeautifulSoup(response.data, "html.parser")
info_box = soup.find('table', {"class": "infobox vevent"})

a = None
for tr in info_box.tbody:
    th = tr.th
    if th is not None:
        if th.text == 'Release date':
            print()
            release = re.findall('\w+\&nbsp\;\d+\,\&nbsp\;\d+', tr.text)
            #release = release.replace('&nbsp', '')
        elif th.text == 'Box office':
            pass
            # this.box_office = re.findall('\$\d+\.\d+\s\w+', tr.td.text)[0]
            # this.box_office.replace('&nbsp', '')
'''

test_spider = scraper.scraper()
test_spider.manual_add("https://en.wikipedia.org/wiki/Avatar_(2009_film)")
test_spider.manual_add("https://en.wikipedia.org/wiki/Tom_Hiddleston")
test_spider.start()
test_spider.complete_all()
test_spider.g.write_to_json('./')

print(test_spider.g.movie_num)
print(test_spider.g.actor_num)
