from bs4 import BeautifulSoup
import urllib3
import queue
import threading
import time
import logging
import re
import random
from Model import models, graph
from datetime import datetime
from dateutil.relativedelta import relativedelta

class scraper:

    def __init__(self):
        self.movie_count = 0
        self.actor_count = 0
        self.movie_max = 125
        self.actor_max = 300
        self.threads_num = 12
        self.urls = queue.Queue()
        self.urls.put('https://en.wikipedia.org/wiki/Avatar_(2009_film)')
        self.threadLock = threading.Lock()
        self.g = graph.graph()

    def manual_add(self, url):
        self.urls.put(url)
        return

    def start(self):
        threads = []
        stops = []

        http = urllib3.PoolManager()
        start = self.urls.get()
        response = http.request('GET', start)
        soup = BeautifulSoup(response.data, "html.parser")
        content_text = soup.find(id='mw-content-text')
        links = content_text.find_all('a')
        for link in links:
            ref = link.get("href")
            if ref is None:
                continue
            if ref.startswith('/wiki/') and 'File' not in ref and 'Award' not in ref:
                refid = self.get_wiki_id(ref)
                if refid != id:
                    self.urls.put("https://en.wikipedia.org" + ref)
        for i in range(self.threads_num):
            s = threading.Event()
            name = "thread " + str(i)
            t = threading.Thread(target=self.parse, args=[name, s])
            t.start()
            threads.append(t)
            stops.append(s)
        print('Start Scraping')
        logging.info('Start Scraping')
        time.sleep(100)
        print('Times up')
        for s in stops:
            s.set()
        logging.info('End Scraping')
        return

    def complete_all(self):
        return

    def parse(self, name, stop_event):
        http = urllib3.PoolManager()
        while not stop_event.is_set():
            url = self.urls.get()
            response = http.request('GET', url)
            soup = BeautifulSoup(response.data, "html.parser")
            navigation = soup.find(id='mw-normal-catlinks')
            cates = navigation.find('ul').text
            if 'television' in cates:
                pass
            elif 'actor' in cates or 'actress' in cates:
                act_name = soup.find(id="firstHeading").text
                content_text = soup.find(id='mw-content-text')
                id = self.get_wiki_id(url)
                self.parse_actor(id, act_name, content_text)
            elif 'film' in cates:
                id = self.get_wiki_id(url)
                content_text = soup.find(id='mw-content-text')
                self.parse_movie(id, content_text)
            else:
                pass # not actor or movie
            self.urls.task_done() # mark task done
            # with self.threadLock:
            #     if self.actor_count >= self.actor_max and self.movie_count >= self.movie_max:
            #         break
            time.sleep(random.random()) # sleep for (0, 1) second
        print(name + ' Done')
        return

    def get_wiki_id(self, url):
        return url.split('/')[-1]

    def parse_movie(self, id, soup):
        with self.threadLock:
            if id in self.g.all_movies:
                return
        info_box = soup.find('table', {"class": "infobox vevent"})
        if info_box is None:
            return
        this = models.films()
        this.id = id
        first = True
        for tr in info_box.tbody:
            th = tr.th
            if th is not None:
                if first:
                    this.name = th.text
                    first = False
                if th.text == 'Starring':
                    for link in tr.find_all('a'):
                        actor_wiki = link.get('href')
                        actor_id = self.get_wiki_id(actor_wiki)
                        this.add_actor(actor_id)
                        self.urls.put("https://en.wikipedia.org" + actor_wiki)
                elif th.text == 'Release date':
                    try:
                        this.release = re.findall('\d+\-\d+\-\d+', tr.td.div.ul.li.text)[0]
                    except IndexError:
                        this.release = re.findall('\d+', tr.text)
                    except AttributeError:
                        this.release = re.findall('\d+', tr.td.text)
                elif th.text == 'Box office':
                        try:
                            bo1 = re.findall('\$\d+\.*\d+\s\w+', tr.td.text)
                            if len(bo1) == 0:
                                bo1 = re.findall('\$.+\d+', tr.td.text)
                            bo1 = bo1[0].replace(',', '')
                            gross = bo1.strip('$')
                            if gross.split()[-1] == 'million':
                                this.box_office = float(gross.split()[0]) * 10e6
                            elif gross.split()[-1] == 'billion':
                                this.box_office = float(gross.split()[0]) * 10e9
                            else:
                                this.box_office = float(gross.split()[0])
                        except Exception:
                            this.box_office = None
                else:
                    pass

        with self.threadLock:
            self.g.add_movie(this)
            self.movie_count += 1
        return

    def parse_actor(self, id, name, soup):
        with self.threadLock:
            if id in self.g.all_actors:
                return

        info_box = soup.find('table', {"class": "infobox biography vcard"})
        if info_box is None:
            return
        this = models.actors()
        this.id = id
        this.name = name
        try:
            birth = info_box.tbody.find('span', {"class":'bday'}).text
            if birth is None:
                age = soup.find("span", {"class":"noprint ForceAgeToShow"}).text
                age = re.findall('\d+', age)[0]
                this.birth = str(datetime.today() - relativedelta(year=int(age)))
            else:
                #this.birth = datetime.strptime(birth, '%Y-%m-%d').date()
                this.birth = birth
        except Exception:
            this.birth = None

        with self.threadLock:
            self.g.add_actor(this)
            self.actor_count += 1


        links = soup.find_all('a')
        for link in links:
            ref = link.get("href")
            if ref is None:
                continue
            if ref.startswith('/wiki/') and 'File' not in ref and 'Award' not in ref:
                refid = self.get_wiki_id(ref)
                if refid != id:
                    self.urls.put("https://en.wikipedia.org" + ref)
        return
