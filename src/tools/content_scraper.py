
import re
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

class ContentScraper:
    @staticmethod
    async def scrape_html(url):
        """
        Sends URL to Playwright to extract HTML contents.

        Args:
            url (str): URL to target website
        
        Returns:
            html_contents (str): The contents of the HTML of the target website
        """
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36")
                page = await context.new_page()
                await page.goto(url)
                html = await page.evaluate('document.body.innerHTML')
                await browser.close()
                return html
            
        except Exception as e:
            error_msg = str(e)
            if "ERR_ABORTED" in error_msg or "net::" in error_msg:
                return f"Cannot access URL {url}: Network error or unsupported file type"
            else:
                return f"Error scraping {url}: {error_msg}"

    @staticmethod
    def declutter_html(soup:BeautifulSoup):
        """
        Removes all HTML elements from BeautifulSoup object that would clutter the page contents.

        Args:
            soup (BeautifulSoup): Contains the HTML contents of the page

        Returns:
            soup (BeautifulSoup): HTML contents with cluttering elements removed
        """

        # headers, navs, and footers typically contain links to other parts of the website
        # L> Excessively clutter context, especially when truncating for keywords
        for element in ['header', 'nav', 'footer']:
            elements = soup.find_all(element)  
            for elm in elements:
                elm.decompose()
        
        # These are all common form elements that can have text
        # Often contain tens of options that just clutter context
        for element in ['select', 'textarea', 'button', 'option']:
            elements = soup.find_all(element)
            for elm in elements:
                elm.decompose()
        
        return soup

    @staticmethod
    def clean_whitespace(soup:BeautifulSoup):
        """
        Converts a BeautifulSoup object to a string while also removing excessive white space from the string.

        Args:
            soup (BeautifulSoup): Contains the HTML contents of the page
        
        Returns:
            contents (str): Webpage contents as a string without excessive white space.
        """

        # Remove excessive white space
        contents = soup.get_text().strip()
        contents = re.sub(r'\n\s*\n+', '\n', contents)
        contents = re.sub(r'^\s+|\s+$', '', contents, flags=re.MULTILINE)

        return contents

    def run(self, url:str, declutter:bool=False):
        raw_html = asyncio.run(self.scrape_html(url))
        soup = BeautifulSoup(raw_html, features='html.parser')
        if declutter:
            soup = self.declutter_html(soup)
        contents = self.clean_whitespace(soup)

        return contents