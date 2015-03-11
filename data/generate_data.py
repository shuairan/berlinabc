import json
from pprint import pprint

from fazcrawler import FazCrawler

json_data=open('berlinabc_simple.json')
data = json.load(json_data)

articles = []
faz = FazCrawler('berlinabc')

print("Starting Crawler")
for entry in data:
    #pprint(entry)
    link = entry['link']
    coords = entry['location']
    
    print("Completing %s" % link)
    rss_data = faz.feed_data(link)
    entry['title'] = rss_data.title
    entry['author'] = rss_data.author
    entry['published'] = rss_data.published
    
    articles.append(entry)
    
json_data.close()
print("Crawling completed")

#print(json.dumps(articles))

article_data = '../articles.json'

with open(article_data, 'w') as outfile:
    json.dump(articles, outfile, indent=4)
    print("Data file written to %s" % article_data)
