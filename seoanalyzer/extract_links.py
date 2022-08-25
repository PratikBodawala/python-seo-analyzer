import time
from urllib.parse import urlparse

def extract_links(url):
    start_time = time.time()

    def calc_total_time():
        return time.time() - start_time

    output = {'pages': set(), 'total_time': calc_total_time()}

    from seoanalyzer.website import Website
    site = Website(url, None, False, False, False, True)

    site.crawl()

    for p in site.crawled_pages:
        urls = p.talk()
        for url in urls:
            url_obj = urlparse(url)
            parsed_url = f'{url_obj.scheme}://{url_obj.netloc}{url_obj.path}'
            output['pages'].add(parsed_url)

    output['pages'] = [p for p in site.pages]

    output['total_time'] = calc_total_time()

    return output
