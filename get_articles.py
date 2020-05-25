import json
import requests
from os import makedirs
from os.path import join, exists
from datetime import date, timedelta

ARTICLES_DIR = join('tempdata', 'articles')
makedirs(ARTICLES_DIR, exist_ok=True)

MY_API_KEY = open('apikey.txt', 'r').read()
API_ENDPOINT = 'http://content.guardianapis.com/search'
my_params = {
    'q': "Coronavirus%20OR%20Covid19%20OR%20Wuhanvirus",
    'from-date': "",
    'to-date': "",
    'order-by': "oldest",
    'show-fields': 'all',
    'show-tags':'all',
    'page-size': 50,
    'api-key': MY_API_KEY
}

# day iteration from here:
# http://stackoverflow.com/questions/7274267/print-all-day-dates-between-two-dates
start_date = date(2019, 12, 1)
end_date = date.today()
dayrange = range((end_date - start_date).days + 1)
for daycount in dayrange:
    dt = start_date + timedelta(days=daycount)
    datestr = dt.strftime('%Y-%m-%d')
    fname = join(ARTICLES_DIR, datestr + '.json')
    if not exists(fname):
        # then let's download it
        print(f"Downloading: {datestr}")
        all_results = []
        my_params['from-date'] = datestr
        my_params['to-date'] = datestr
        current_page = 1
        total_pages = 1
        while current_page <= total_pages:
            print(f"...{current_page} page/ {total_pages} pages")
            my_params['page'] = current_page
            resp = requests.get(API_ENDPOINT, my_params)
            data = resp.json()
            all_results.extend(data['response']['results'])
            # if there is more than one page
            current_page += 1
            total_pages = data['response']['pages']

        with open(fname, 'w') as f:
            print("Writing to", fname)

            # re-serialize it for pretty indentation
            f.write(json.dumps(all_results, indent=2))
