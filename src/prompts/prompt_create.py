
from langchain_core.prompts import ChatPromptTemplate

from ..utils import parser

with open("src/prompts/agent_instructions.txt", encoding="utf-8", mode='r') as file:
    agent_instructions = file.read()

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a student counselor aimed at helping students find extracurricular opportunities.
            You will find the desired program and output it in the format below so that your colleagues can display the information clearly to students. 
            \n{agent_instructions}
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions(), agent_instructions=agent_instructions)