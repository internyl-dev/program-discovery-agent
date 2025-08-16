import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor

from .prompts import prompt
from .tools import file_save, ddgs_run, url_visit
from .schemas import RootSchema
from .utils import parse_raw_response

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_MODEL"),
    api_version="2024-05-01-preview",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
    )

tools = [file_save, ddgs_run, url_visit]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("What extracurricular program are you looking for?\n")
raw_response = agent_executor.invoke({"query": query})

parse_raw_response(raw_response)