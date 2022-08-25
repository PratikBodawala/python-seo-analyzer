from pprint import pprint

from seoanalyzer.extract_links import extract_links
import csv

base_url = 'http://localhost:3000'

with open('scratch_37.txt', 'r') as url_file:
    with open('seo-report.csv', 'w') as csv_file:
        csv_data = csv.DictWriter(csv_file,
                                  ['page', 'title', 'desc', 'og:title', 'og:description', 'og:url', 'og:image'], )
        csv_data.writeheader()
        for i, relative_url in enumerate(url_file, start=1):
            relative_url = relative_url.strip()
            full_url = f'{base_url}{relative_url}'
            print(i, full_url)
            data = extract_links(full_url)
            # page = data.pop('pages')[0]
            pprint(data)
            # pprint(page)
            # info = page.get('additional_info')
            # csv_data.writerow(
            #     {'page': page.get('url'),
            #      'title': page.get('title'),
            #      'desc': page.get('description'),
            #      # 'og:title': info.get('og_title')[0] if info.get('og_title') else None,
            #      # 'og:description': info.get('og_desc')[0] if info.get('og_desc') else None,
            #      # 'og:url': info.get('og_url')[0] if info.get('og_url') else None,
            #      # 'og:image': info.get('og_image')[0] if info.get('og_image') else None
            # })
            break
