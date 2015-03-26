import feedparser
import re
from datetime import datetime
import locale

"""
Crawl the FAZ feed for a blog.faz.net

there is a basic feed: http://blogs.faz.net/BLOGNAME/feed
but it only returns the 10 last items.
so we use http://blogs.faz.net/BLOGNAME/YEAR/MONTH/feed
for 10 items a month and if the given link is not in there we crawl:
http://blogs.faz.net/BLOGNAME/YEAR/MONTH/DAY/feed
if there are more than 10 entries a day we have a problem.

"""

locale.setlocale(locale.LC_ALL, 'de_DE')

def fazDateHandler(aDateString):
    return datetime.strptime(aDateString, "%a, %d %b %Y %H:%M:%S %z")
    
feedparser.registerDateHandler(fazDateHandler)

class FazFeedCrawler():
    def __init__(self, blogname):
        self.blogname = blogname
        self.rss_data = []
        self.links = []
        
    def feed_data(self, url):
        if url not in self.links:
            print("Data not found, try to crawl it")
            self.crawl(url)
        return self.get_feed_data_entry(url)
        
    def get_feed_url_from_link(self, url, specific=False):
        rex = r'(http:\/\/.*\/%s\/[0-9]{4}\/[0-9]{2}\/)([0-9]{2}\/)' % self.blogname
        match = re.match(rex, url)
        return match.group(1) + (match.group(2) if specific else "") + "feed"
        
    def get_feed_data_entry(self, url):
        for article in self.rss_data:
            if article.link == url:
                return article
        print("Could not find data in feed for %s" % url)
        return None 

    def crawl(self, url, specific=False):
        feed_url = self.get_feed_url_from_link(url, specific)
        data = self.crawl_feed_data(feed_url)
        
        self.add_feed_data(data)
        #print(self.links)
        
        if url in self.links:
            return
        
        if not specific:
            """ maybe more than 10 items -> crawl specific sub feed """
            self.crawl(url, True)
        else:
            raise Exception("Could not get data from FAZ for %s" % url)
        
    def add_feed_data(self, data):
        for article in data.entries:
            self.links.append(article.link)
            self.rss_data.append(article)
        #self.rss_data.append(data.entries)
        
    def crawl_feed_data(self, feed_url):
        print("Crawling %s" % feed_url)
        feed = feedparser.parse(feed_url)
        return feed

