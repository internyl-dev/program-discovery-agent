
from langchain_core.prompts import ChatPromptTemplate

from .assets.prompts import PROMPTS
from ..utils import ResponseParser

class PromptCreator:
    def __init__(self, section:str):
        self.agent_instructions = PROMPTS[section]
        self.parser = ResponseParser(section).parser

    def create_chat_prompt_template(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You will be given a partially filled JSON object.
                    Your job is to search for information to completely populate the schema.
                    The schema and search instructions will be given below:
                    \n{agent_instructions}
                    Wrap the output in this format and provide no other text\n{format_instructions}
                    """,
                ),
                ("placeholder", "{chat_history}"),
                ("human", "{query}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        ).partial(format_instructions=self.parser.get_format_instructions(), agent_instructions=self.agent_instructions)