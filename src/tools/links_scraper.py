import re
from bs4 import BeautifulSoup

from .content_scraper import ContentScraper

class LinkScraper(ContentScraper):

    def __init__(self):
        super().__init__()

    @staticmethod
    def is_link(s):
        if '#' in s:
            return False
        
        pattern = re.compile(
            r'^('
            r'https?://[\w.-]+\.[a-zA-Z]{2,}(/[^\s]*)?'  # full URL
            r'|'
            r'//[\w.-]+\.[a-zA-Z]{2,}(/[^\s]*)?'         # scheme-relative
            r'|'
            r'/[^\s]*'                                   # relative path
            r'|'
            r'[\w.-]+\.[a-zA-Z]{2,}(/[^\s]*)?'           # bare domain
            r')$',
        )
        return bool(pattern.match(s))
    
    @staticmethod
    def process_link(url:str, href:str):
        if href[0] == '/':
            return '/'.join(url.split('/')[0:3]) + href

        elif href[0:7] == 'http://' or href[0:8] == 'https://':
            return href

        elif href[-1] == '/':
            if not url[-1] == '/':
                url += '/'
            return url + href

    def scrape_all_links(self, soup:BeautifulSoup, url:str):
        new_links = {}
        links = soup.find_all('a')

        for link in links:
            try:
                # Add link to dictionary with the associated text being the key
                # L> For future filtering based off of keywords
                href = link.get('href').strip()
                text = link.get_text().strip()
                
                if self.is_link(href):
                    href = self.process_link(url, href)
                    new_links[text] = href

            except Exception: 
                continue

        return new_links
    
    def run(self, url):
        soup = BeautifulSoup(
            self.scrape_html(url), 
            features="html.parser")
        return self.scrape_all_links(soup, url)