import re
from bs4 import BeautifulSoup
from typing import Optional

from .content_scraper import ContentScraper

class LinkScraper:

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def is_link(s) -> bool:
        """Returns true if a string is a valid base_url"""
        if '#' in s:
            return False
        
        pattern = re.compile(
            r'^('
            r'https?://[\w.-]+\.[a-zA-Z]{2,}(/[^\s]*)?'  # full base_url
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
    def process_link(base_url:str, href:str) -> str:
        """Returns a valid base_url given a base base_url and a target HREF"""
        if href[0] == '/':
            return '/'.join(base_url.split('/')[0:3]) + href

        elif href[0:7] == 'http://' or href[0:8] == 'https://':
            return href

        elif href[-1] == '/':
            if not base_url[-1] == '/':
                base_url += '/'
            return base_url + href

        else: raise TypeError

    def scrape_all_links(self, soup:BeautifulSoup, base_url:str) -> dict:
        """Scrapes all links from some HTML contents"""
        new_links = {}
        links = soup.find_all('a')

        for link in links:
            try:
                # Add link to dictionary with the associated text being the key
                # L> For future filtering based off of keywords
                href = link.get('href')
                if isinstance(href, str):
                    href.strip()
                text = link.get_text().strip()
                
                if self.is_link(href) and isinstance(href, str):
                    href = self.process_link(base_url, href)
                    new_links[text] = href

            except Exception: 
                continue

        return new_links
    
    def run(self, base_url, scraper:Optional[ContentScraper]=None) -> dict:
        """Returns a dictionary of all links in the format {text : href}"""
        scraper = scraper or ContentScraper()
        soup = BeautifulSoup(
            scraper.scrape_html(base_url), 
            features="html.parser")
        return self.scrape_all_links(soup, base_url)