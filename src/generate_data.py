import json
import itertools
from pprint import pprint
import re

from fazcrawler import FazFeedCrawler#, FazHttpCrawler
import wikicrawler

def get_station_match(candidates):
    print(candidates)
    for candidate in candidates:
        matches = list(filter(lambda s: candidate in s, stations))
        if matches:
            print("Candidate %s has match %s" % (candidate, matches))
            return matches[0]
    return None

def find_station(article):
    candidates = []
    
    candidates.append(article["title"])
    alphanumeric = re.sub('[^0-9a-zA-Zäöüß]+', ' ', article["title"])
    candidates.append(alphanumeric)
    candidates.extend(alphanumeric.split(" "))
    candidates.extend(article["tags"])
    candidates = [c for c in candidates if len(c) > 5]
    station = get_station_match(candidates)
    
    if station is None:
        print("no station for %s (%s)" % (article["title"], candidates))
    return station


def get_coordinates(station):
    coords = wikicrawler.get_coordinates(station)
    print("Coords", coords) 
    return coords
    #print("Find coords for %s (%s)" % (article["title"], article["link"]))
    #print(list(matches))
    #for station in stations:    

def main():
    # get list of stations from Wikipedia:
    print("Crawlink Wikipedia for stations")
    wikicat = [ 'Kategorie:Bahnhof_der_S-Bahn_Berlin', 'Kategorie:U-Bahnhof_in_Berlin' ]
    stations = list(itertools.chain(* [wikicrawler.get_page_list(s) for s in wikicat]))

    # get all blog article links from FAZ:
    print("Crawling blog.faz.net for article links")
    #faz_http = FazHttpCrawler('berlinabc')
    # TODO: get all blog links from http page

    faz = FazFeedCrawler('berlinabc')

    json_data=open('berlinabc_simple.json')
    berlinabc_links = json.load(json_data)

    articles = []
    print("Starting Crawler")
    for entry in berlinabc_links:
        #pprint(entry)
        link = entry['link']
        entry['location'] = ''
        
        print("\nCompleting %s" % link)
        rss_data = faz.feed_data(link)
        #pprint(rss_data)
        
        entry['title'] = rss_data.title
        entry['description'] = rss_data.description
        entry['tags'] = [tag['term'] for tag in rss_data.tags]
        entry['author'] = rss_data.author
        entry['published'] = rss_data.published
        #pprint(entry)
        station = find_station(entry)
        if station:
            coords = get_coordinates(station)
            entry['coordinates'] = coords

        articles.append(entry)
        
    json_data.close()
    print("Crawling completed")

    #print(json.dumps(articles))

    article_data = '../articles.json'

    with open(article_data, 'w') as outfile:
        json.dump(articles, outfile, indent=4)
        print("Data file written to %s" % article_data)
        
if __name__ == "__main__":
    main()
