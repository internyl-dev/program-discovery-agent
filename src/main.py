import os
import copy
from pprint import pp
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor

from .firebase import FirebaseClient
from .prompts import PromptCreator
from .tools import ddgs_run, content_scraper, links_scraper
from .utils import ResponseParser, denest_dict, callbacks, logger

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_MODEL"),
    api_version="2024-05-01-preview",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
    )

collection_to_read = "internships-history"
collection_to_add = "programs-display"

firebase = FirebaseClient()

documents = firebase.read_documents(collection_to_read)
document = list(documents.values())[0]
new_document = copy.deepcopy(document)

for section in ["overview", "eligibility", "dates", "locations", "costs", "contact"]:

    _denested_dict = denest_dict(new_document[section])

    if not any((_denested_dict[key] == "not provided") for key in _denested_dict):
        logger.info(f"Skipped {section}")
        continue

    prompt = PromptCreator().create_chat_prompt_template(section)
    tools = [ddgs_run, content_scraper, links_scraper]
    agent = create_tool_calling_agent(
        llm=llm,
        prompt=prompt,
        tools=tools
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    query = new_document
    raw_response = agent_executor.invoke({"query": query}, config={"callbacks": callbacks})

    try:
        new_document[section] = ResponseParser().parse_raw_response(raw_response, section)
    except Exception as e:
        pp(e)

firebase.add_indexed_document(collection_to_add, new_document)
firebase.delete_document(collection_to_read, list(documents.keys())[0])

print('\n\n\n')
pp(document)
print('->')
pp(new_document)