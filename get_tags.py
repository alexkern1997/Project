import json
import requests
from os import makedirs
from os.path import join, exists
from datetime import date
import time

TAGS_DIR = join('tempdata', 'tags')
makedirs(TAGS_DIR, exist_ok=True)

MY_API_KEY = open('apikey.txt', 'r').read()
API_ENDPOINT = 'http://content.guardianapis.com/tags'
my_params = {
    'q': "corona",
    'page-size': 1000,
    'api-key': MY_API_KEY
}
today = date.today()
datestr = today.strftime("%Y-%m-%d")
filename = join(TAGS_DIR, datestr + '.json')

if not exists(filename):
    print(f"Downloading: {datestr} tags!")
    all_results = []
    current_page = 1
    total_pages = 1
    while current_page <= total_pages:
        resp = requests.get(API_ENDPOINT, my_params)
        data = resp.json()
        if data['response']['status'] == 'error':
            error_message = data['response']['message']
            print('API error')
            print(f'Message: {error_message}')
            break
        else:
            print(f"...{current_page} page/ {total_pages} pages")
            my_params['page'] = current_page
            total_pages = data['response']['pages']
            all_results.extend(data['response']['results'])
            # if there is more than one page
            current_page += 1
            time.sleep((1/12.1))

    with open(filename, 'w') as f:
        print("Writing to", filename)
        # re-serialize it for pretty indentation
        f.write(json.dumps(all_results, indent=2))
