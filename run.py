from pprint import pprint

from seoanalyzer.analyzer import analyze
import csv

# base_url = 'http://localhost:3000'
base_url = 'https://noyelling.com.au'

with open('/home/pratik/.config/JetBrains/PyCharm2022.2/scratches/scratch_37.txt', 'r') as url_file:
    with open('/home/pratik/Documents/noyelling/seo-report.csv', 'w') as csv_file:
        csv_data = csv.DictWriter(csv_file,
                                  ['page', 'title', 'desc', 'og:title', 'og:description', 'og:url', 'og:image'], )
        csv_data.writeheader()
        for i, relative_url in enumerate(url_file, start=1):
            relative_url = relative_url.strip()
            full_url = f'{base_url}{relative_url}'
            print(i, full_url)
            data = analyze(full_url, analyze_headings=True, analyze_extra_tags=True, follow_links=False)
            data.pop('keywords')
            page = data.pop('pages')[0]
            pprint(data)
            page.pop('bigrams')
            page.pop('trigrams')
            page.pop('keywords')
            page.pop('warnings')
            page.pop('headings')
            pprint(page)
            info = page.get('additional_info')
            csv_data.writerow(
                {'page': page.get('url'),
                 'title': page.get('title'),
                 'desc': page.get('description'),
                 'og:title': info.get('og_title')[0] if info.get('og_title') else None,
                 'og:description': info.get('og_desc')[0] if info.get('og_desc') else None,
                 'og:url': info.get('og_url')[0] if info.get('og_url') else None,
                 'og:image': info.get('og_image')[0] if info.get('og_image') else None})
            # break
