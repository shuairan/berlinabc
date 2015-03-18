import urllib.request
import urllib.parse
import json

WIKIPEDIA_API="https://de.wikipedia.org/w/api.php"


def wiki_request(params):
    data = urllib.parse.urlencode(params)
    #print(WIKIPEDIA_API + '?' + data)
    data = data.encode('utf-8')
    request = urllib.request.Request(WIKIPEDIA_API)
    
    f = urllib.request.urlopen(request, data)
    str_response = f.read().decode('utf-8')
    return json.loads(str_response)

def get_coordinates(title):
    """ https://de.wikipedia.org/w/api.php?action=query&prop=coordinates&titles=TITEL """
    params = {
        'action': 'query',
        'prop': 'coordinates',
        'format' : 'json',
        'continue' : '',
        'titles': title
    }
    json = wiki_request(params)
    page = json['query']['pages']
    return [(c[0]['lat'], c[0]['lon']) for c in [page[key]['coordinates'] for key in page]][0]

def get_pages_from_category(category):
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
    return wiki_request(params)

def get_page_list(category):
    json = get_pages_from_category(category)
    return [page["title"] for page in json["query"]["categorymembers"]]
