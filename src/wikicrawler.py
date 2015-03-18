import urllib.request
import urllib.parse
import json
import itertools
import re

WIKIPEDIA_API="https://de.wikipedia.org/w/api.php"

class WikiCrawler():
    def get_pages_from_category(self, category):
        """ http://de.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtype=page&cmlimit=500&cmtitle=CATEGORY """
        params = {
            'action': 'query',
            'list': 'categorymembers',
            'format' : 'json',
            'cmtype' : 'page',
            'cmlimit': 500,
            'continue' : '',
            'cmtitle' : category
        }
        json = self.wiki_request(params)
        return [page["title"] for page in json["query"]["categorymembers"]]

    def get_coordinates(self, title):
        """ https://de.wikipedia.org/w/api.php?action=query&prop=coordinates&titles=TITEL """
        params = {
            'action': 'query',
            'prop': 'coordinates',
            'format' : 'json',
            'continue' : '',
            'titles': title
        }
        json = self.wiki_request(params)
        page = json['query']['pages']
        return [(c[0]['lat'], c[0]['lon']) for c in [page[key]['coordinates'] for key in page]][0]

    def wiki_request(self, params):
        data = urllib.parse.urlencode(params)
        #print(WIKIPEDIA_API + '?' + data)
        data = data.encode('utf-8')
        request = urllib.request.Request(WIKIPEDIA_API)
        
        f = urllib.request.urlopen(request, data)
        str_response = f.read().decode('utf-8')
        return json.loads(str_response)

class Candidates():
    def __init__(self):
        self.candidates = []
        self.seen = set()
        self.blacklist = ['Bahnhof', 'Berlin', 'Liste', 'der', 'Bahnhöfe', 'Raum']
        
    def add(self, candidate):
        if not candidate in self.seen and len(candidate) >= 4 and not candidate in self.blacklist:
            self.seen.add(candidate)
            self.candidates.append(candidate)
    
    def addList(self, clist):
        #Todo: Improve!
        for c in clist:
            self.add(c)
    
    def addString(self, string):
        self.add(string)
        title_alpha = re.sub('[^0-9a-zA-Zäöüß]+', ' ', string)
        self.add(title_alpha)
        self.addList(title_alpha.split(" "))
    
    def get(self):
        return self.candidates
        
    def empty(self):
        self.seen = set()
        self.candidates = []
        
class WikiStationCrawler(WikiCrawler):
    def __init__(self, categories):
        self.categories = categories
        self.stations = self.get_station_list(categories)
        
    def get_station_list(self, categories):
        return list(itertools.chain(* [self.get_pages_from_category(s) for s in categories]))

    def get_station_match(self, candidates):
        #print(candidates)
        for candidate in candidates:
            matches = list(filter(lambda s: candidate in s, self.stations))
            if matches:
                #print("Candidate %s has match %s" % (candidate, matches))
                return matches[0]
        return None

    def find_station(self, article):
        candidates = Candidates()
        candidates.addString(article["title"])
        candidates.addList(article["tags"])
        station = self.get_station_match(candidates.get())
        
        if station is None:
            print("no station for %s (%s)" % (article["title"], candidates.get()))
            print("trying to find one from description")
            candidates.empty()
            candidates.addString(article["description"])
            station = self.get_station_match(candidates.get())
            print("Found %s" % station)
        return station
