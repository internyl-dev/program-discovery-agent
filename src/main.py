import os
from pprint import pp
from dotenv import load_dotenv
import json
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor

from src.io.firebase import FirebaseClient
from src.prompts import PromptCreator
from src.tools import ddgs_run, content_scraper, links_scraper

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_MODEL"),
    api_version="2024-05-01-preview",
    temperature=0,
    timeout=None,
    max_retries=2
    )

prompt = PromptCreator().create_chat_prompt_template()
tools = [ddgs_run, content_scraper, links_scraper]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = "Find either virutal extracurricular programs in any US state or in-person extracurricular programs in NYC."
raw_response = agent_executor.invoke({"query": query})

pp(raw_response)

response_dict = json.loads(raw_response["output"])

for url in response_dict["programs"]:
    FirebaseClient.get_instance().save("scrape-queue", {"url": url})