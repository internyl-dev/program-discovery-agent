
from langchain.tools import Tool

from .file_save import save_to_txt
from .ddgs_run import DuckDuckGoSearchRun
from .url_visit import WebScraper

file_save = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file."
)

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

print("Tools initialized")