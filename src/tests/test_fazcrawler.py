import unittest
 
from fazcrawler import FazCrawler

class TestGeoArticle(unittest.TestCase):
    
    def setUp(self):
        self.faz = FazCrawler()
    
    def test_crawler_get_feed_link(self):
        link = "http://blogs.faz.net/berlinabc/2015/02/03/bellevue-31/"
        feedurl = self.faz.get_feed_url_from_link(link)
        self.assertEqual(feedurl, "http://blogs.faz.net/berlinabc/2015/02/feed")

    def test_crawler_get_feed_link_specific(self):
        link = "http://blogs.faz.net/berlinabc/2015/02/03/bellevue-31/"
        feedurl = self.faz.get_feed_url_from_link(link, True)
        self.assertEqual(feedurl, "http://blogs.faz.net/berlinabc/2015/02/03/feed")
