import os
from pprint import pp
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor

from .firebase import firebase
from .prompts import PromptCreator
from .tools import ddgs_run, content_scraper, links_scraper
from .utils import callbacks

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

prompt = PromptCreator().create_chat_prompt_template()
tools = [ddgs_run, content_scraper, links_scraper]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = "Find either virutal extracurricular programs in any US state or in-person extracurricular programs in NYC."
raw_response = agent_executor.invoke({"query": query}, config={"callbacks": callbacks})

pp(raw_response)