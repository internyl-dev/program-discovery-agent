# Internyl Program Discovery Agent

Internyl Website Repo: https://github.com/internyl-dev/internyl-frontend<br>
Internyl Data Acquisition Repo: https://github.com/internyl-dev/internyl-ai-wrapper/tree/refactor<br>
Internyl Website: https://internyl.org

## Table of Contents
1. [How to use](#how-to-use)
    - [Add API Keys](#add-api-keys)
    - [Run main](#run-main)
2. [How it works](#how-it-works)
    - [Models](#models)
    - [Tools](#tools)

## How to use
### Add API Keys
1. Navigate to .env and input any API keys you may have there

### Run main
```
# 1. Create a virtual environment
python -m venv .venv

# 2. Activate the virtual environment
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.venv/scripts/activate

# 3. Install requirements
pip install -r requirements.txt
playwright install

# 4. Run run.py
python run.py
```

## How it works
The discovery agent utilizes a LangChain agent execution chain to perform the agentic behavior. All it does is take a specific set of instructions written to look for programs not already put on a given section of the database (in our case, programs-display) and look specifically for a webpage containing just one internship and its overview information. 

### Models
**Output** - `programs: List[HttpUrl]`<br>
This stores the programs the agent finds as a list of URLs.

### Tools
**Search** - `search (search_term:str, max_results:int)`<br>
Using the DDGS search module, return the search results given a search term.<br><br>
**Visit URL** - `visit_url (url:str)`<br>
Using Playwright return the parsed webpage contents of a URL.<br><br>
**Get All Links** - `get_all_links (url:str)`<br>
Using Playwright return all URLs found within a webpage.
