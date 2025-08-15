import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

from tools import *
from schemas import *

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_MODEL"),
    api_version="2024-05-01-preview",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
    )

parser = PydanticOutputParser(pydantic_object=RootSchema)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a student counselor aimed at helping students find extracurricular opportunities.
            Help the user find and understand their desired program and use neccessary tools. 
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("What extracurricular program are you looking for?\n")
raw_response = agent_executor.invoke({"query": query})

try:
    # The output is already a string, not a list with a text field
    raw_output = raw_response.get("output")
    
    # Remove the 'json' prefix if it exists
    if raw_output.startswith('json\n'):
        raw_output = raw_output[5:]  # Remove 'json\n'
    
    structured_response = parser.parse(raw_output)
    print(structured_response)
    
except Exception as e:
    print("Error parsing response", e)
    print("Raw Response - ", raw_response)
    print("Output content - ", raw_response.get("output"))