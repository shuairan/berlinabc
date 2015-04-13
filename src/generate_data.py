import json
from pprint import pprint
from datetime import datetime
import time

from fazcrawler import FazFeedCrawler#, FazHttpCrawler
from wikicrawler import WikiStationCrawler

wikicat = [ 'Kategorie:Bahnhof_der_S-Bahn_Berlin', 'Kategorie:U-Bahnhof_in_Berlin' ]   

def generate_base_data_entry(title, link, description, tags, author, published):
    entry = {}
    entry['title'] = title
    entry['link'] = link
    entry['description'] = description
    entry['tags'] = tags
    entry['author'] = author
    entry['published'] = published
    return entry
    
def generate_article_data(station, coords):
    data = {}
    data['articles'] = []
    
    if station is "none":
        return data
        
    data['name'] = station
    data['wikipedia_link'] = "https://de.wikipedia.org/wiki/" + station.replace(' ', '_')
    data['coordinates'] = coords
    
    return data

def main():
    # get list of stations from Wikipedia:
    print("Crawlink Wikipedia for stations")
    wiki = WikiStationCrawler(wikicat)
    
    # get all blog article links from FAZ:
    print("Crawling blog.faz.net for article links")
    #faz_http = FazHttpCrawler('berlinabc')
    # TODO: get all blog links from http page

    faz = FazFeedCrawler('berlinabc')

    json_data=open('berlinabc_simple.json')
    berlinabc_links = json.load(json_data)

    markers = {}
    print("Starting Crawler")
    for article in berlinabc_links:
        link = article['link']
        
        print("\nCompleting %s" % link)
        rss_data = faz.feed_data(link)
        #pprint(rss_data)

        entry = generate_base_data_entry(
            title = rss_data.title,
            link = link,
            description = rss_data.description,
            tags = [tag['term'] for tag in rss_data.tags],
            author = rss_data.author,
            published = time.strftime('%d. %b, %Y', rss_data.published_parsed)
        )

        #pprint(entry)
        station = wiki.find_station(entry)
        
        if station and not station in markers:
            coords = wiki.get_coordinates(station)
            markers[station] = generate_article_data(station, coords)
            
        if station in markers:
            markers[station]['articles'].append(entry)
        
    json_data.close()
    print("Crawling completed")

    #print(json.dumps(articles))

    article_data = '../markers.json'

    with open(article_data, 'w') as outfile:
        json.dump(markers, outfile, indent=4, sort_keys=True)
        print("Data file written to %s" % article_data)
        
if __name__ == "__main__":
    main()
