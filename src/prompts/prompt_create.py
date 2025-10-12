
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from .assets.prompt import PROMPT
from ..models import Output

class PromptCreator:

    def create_chat_prompt_template(self):
        agent_instructions = PROMPT
        parser = PydanticOutputParser(pydantic_object=Output)
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You will be given a dictionary of information for extracurricular programs.
                    Your job is to search for more extracurricular programs, not returning the programs already given.
                    The instructions will be given below:
                    \n{agent_instructions}
                    Wrap the output in this format and provide no other text\n{format_instructions}
                    """,
                ),
                ("placeholder", "{chat_history}"),
                ("human", "{query}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        ).partial(format_instructions=parser.get_format_instructions(), agent_instructions=agent_instructions)

        return prompt