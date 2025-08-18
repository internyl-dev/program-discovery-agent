
from langchain.tools import Tool

from .ddgs_run import DuckDuckGoSearchRun
from .url_visit import WebScraper
from .links_scrape import LinkScraper

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

url_visit = Tool(
    name="visit_url",
    func=WebScraper().run,
    description=(
    "Use this tool to extract the information from a website.\n"
    "Parameters:\n"
    " - url (str): The url to extract the contents from."
    )
)

links_scrape = Tool(
    name="get_all_links",
    func=LinkScraper().run,
    description=(
    "Use this tool to extract all links from within a website.\n"
    "Parameters:\n"
    " - url (str): The url to extract the links from."
    )
)

print("Tools initialized")