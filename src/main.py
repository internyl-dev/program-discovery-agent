import os
import copy
from pprint import pp
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor

from .firebase import FirebaseClient
from .prompts import PromptCreator
from .tools import ddgs_run, url_visit, links_scrape
from .utils import ResponseParser

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_MODEL"),
    api_version="2024-05-01-preview",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
    )

firebase = FirebaseClient()
document = firebase.read_documents("internships-history")[2]
new_document = copy.deepcopy(document)

for section in ["eligibility"]:

    prompt = PromptCreator().create_chat_prompt_template(section)

    tools = [ddgs_run, url_visit, links_scrape]
    agent = create_tool_calling_agent(
        llm=llm,
        prompt=prompt,
        tools=tools
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    query = new_document
    raw_response = agent_executor.invoke({"query": query})

    try:
        new_document[section] = ResponseParser().parse_raw_response(raw_response, section)
    except Exception as e:
        print(e)

pp(document)
print('->')
pp(new_document)