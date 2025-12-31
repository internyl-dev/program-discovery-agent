
from langchain.tools import Tool

from .ddgs_run import DuckDuckGoSearchRun
from .content_scraper import ContentScraper
from .links_scraper import LinkScraper

ddgs_run = Tool(
    name="search",
    func=DuckDuckGoSearchRun,
    description=(
    "Use this tool to search the web for information.\n"
    "Parameters:\n"
    " - query (str): The search term or question.\n"
    " - max_results (int, optional): The number of results to return (default 5)."
    )
)

content_scraper = Tool(
    name="visit_url",
    func=ContentScraper().run,
    description=(
    "Use this tool to extract the information from a website. Use this to understand the website contents.\n"
    "Parameters:\n"
    " - url (str): The url to extract the contents from."
    )
)

links_scraper = Tool(
    name="get_all_links",
    func=LinkScraper().run,
    description=(
    "Use this tool to extract all links from within a website. Use this to navigate through the website.\n"
    "Parameters:\n"
    " - url (str): The url to extract the links from."
    )
)

print("Tools initialized")