import json
from pprint import pprint

from fazcrawler import FazFeedCrawler#, FazHttpCrawler
from wikicrawler import WikiStationCrawler

wikicat = [ 'Kategorie:Bahnhof_der_S-Bahn_Berlin', 'Kategorie:U-Bahnhof_in_Berlin' ]   

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
        station = wiki.find_station(entry)
        if station:
            entry['station'] = station
            entry['wikipedia_link'] = "https://de.wikipedia.org/wiki/" + station.replace(' ', '_')
            coords = wiki.get_coordinates(station)
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
