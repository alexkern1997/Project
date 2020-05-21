import json
import requests
from os import makedirs
from os.path import join, exists
from datetime import date
import time

TAGS_DIR = join('tempdata', 'sections')
makedirs(TAGS_DIR, exist_ok=True)

MY_API_KEY = open('apikey.txt', 'r').read()
API_ENDPOINT = 'http://content.guardianapis.com/sections'
my_params = {
    'api-key': MY_API_KEY
}
today = date.today()
datestr = today.strftime("%Y-%m-%d")
filename = join(TAGS_DIR, datestr + '.json')

if not exists(filename):
    print(f"Downloading: {datestr} sections!")
    all_results = []
    resp = requests.get(API_ENDPOINT, my_params)
    data = resp.json()
    if data['response']['status'] == 'error':
        error_message = data['response']['message']
        print('API error')
        print(f'Message: {error_message}')
    else:
        all_results.extend(data['response']['results'])
        time.sleep((1/12.1))

    with open(filename, 'w') as f:
        print("Writing to", filename)
        # re-serialize it for pretty indentation
        f.write(json.dumps(all_results, indent=2))
