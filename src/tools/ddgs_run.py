
from ddgs import DDGS

def DuckDuckGoSearchRun(query:str, max_results:int=5):
    return DDGS().text(query=query, max_results=max_results)