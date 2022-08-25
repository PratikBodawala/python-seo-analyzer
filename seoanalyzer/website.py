from collections import Counter
from collections import defaultdict
from urllib.parse import urlsplit, urlparse
from xml.dom import minidom

import socket

from seoanalyzer.http import Http
from seoanalyzer.page import Page

class Website():
    def __init__(self, base_url, sitemap, analyze_headings, analyze_extra_tags, follow_links, one_type_follow):
        self.base_url = base_url
        self.sitemap = sitemap
        self.analyze_headings = analyze_headings
        self.analyze_extra_tags = analyze_extra_tags
        self.follow_links = follow_links
        self.crawled_pages = []
        self.crawled_urls = set([])
        self.page_queue = []
        self.wordcount = Counter()
        self.bigrams = Counter()
        self.trigrams = Counter()
        self.content_hashes = defaultdict(set)
        self.one_time_follow = one_type_follow
        self.pages = set()

    def check_dns(self, url_to_check):
        try:
            o = urlsplit(url_to_check)
            socket.gethostbyname(o.hostname)
            return True
        except:
            pass

        return False

    def get_text_from_xml(self, nodelist):
        """
        Stolen from the minidom documentation
        """
        rc = []

        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)

        return ''.join(rc)

    def crawl(self):
        http = Http()
        if self.sitemap:
            page = http.get(self.sitemap)
            if self.sitemap.endswith('xml'):
                xmldoc = minidom.parseString(page.data.decode('utf-8'))
                sitemap_urls = xmldoc.getElementsByTagName('loc')
                for url in sitemap_urls:
                    self.page_queue.append(self.get_text_from_xml(url.childNodes))
            elif self.sitemap.endswith('txt'):
                sitemap_urls = page.data.decode('utf-8').split('\n')
                for url in sitemap_urls:
                    self.page_queue.append(url)

        self.page_queue.append(self.base_url)

        for url in self.page_queue:
            if url in self.crawled_urls:
                continue

            page = Page(url=url, base_domain=self.base_url,
                        analyze_headings=self.analyze_headings,
                        analyze_extra_tags=self.analyze_extra_tags)

            if page.parsed_url.netloc != page.base_domain.netloc:
                continue

            page.analyze()

            self.content_hashes[page.content_hash].add(page.url)
            url_obj = urlparse(url)
            parsed_url = f'{url_obj.scheme}://{url_obj.netloc}{url_obj.path}'
            self.pages.add(parsed_url)
            for w in page.wordcount:
                self.wordcount[w] += page.wordcount[w]

            for b in page.bigrams:
                self.bigrams[b] += page.bigrams[b]

            for t in page.trigrams:
                self.trigrams[t] += page.trigrams[t]

            self.page_queue.extend(page.links)

            self.crawled_pages.append(page)
            self.crawled_urls.add(page.url)
            counter = 0
            if self.one_time_follow:
                counter += 1
                if counter > 1:
                    break
            else:
                if not self.follow_links:
                    break
