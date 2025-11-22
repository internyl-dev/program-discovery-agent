
from ddgs import DDGS

def DuckDuckGoSearchRun(query:str, max_results:int=5):
    """Returns search results given a query with the DDGS API"""
    return DDGS().text(query=query, max_results=max_results)