import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor

from .firebase import FirebaseClient
from .prompts import PromptCreator
from .tools import file_save, ddgs_run, url_visit
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

prompt = PromptCreator().create_chat_prompt_template("eligibility")

tools = [file_save, ddgs_run, url_visit]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

firebase = FirebaseClient()
document = firebase.read_documents("internships-history")[0]

query = document
raw_response = agent_executor.invoke({"query": query})

ResponseParser().parse_raw_response(raw_response, "eligibility")