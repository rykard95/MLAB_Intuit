import json
from urllib.request import urlopen
from urllib.parse import urlencode


def describe(query):
    api_key = 'AIzaSyAMe0hZkE-Sr2lTrOR4oO54IzNModGTnTs'
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': query,
        'limit': 1,
        'indent': True,
        'key': api_key,
        }
    url = service_url + '?' + urlencode(params)
    response = json.loads(str(urlopen(url).read(), 'utf-8'))
    if 'itemListElement' in response:
        if len(response['itemListElement']) > 0:
            if 'result' in response['itemListElement'][0]:
                if 'description' in response['itemListElement'][0]['result']:
                    return response['itemListElement'][0]['result']['description']
