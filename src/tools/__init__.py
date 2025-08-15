from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool

from .save_tool import save_to_txt
from.search_tool import search

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file.",
)

search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information",
)

print("Tools initialized")