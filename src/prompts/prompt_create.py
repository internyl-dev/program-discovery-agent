
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from .assets.prompts import PROMPTS
from ..schemas import schemas

class PromptCreator:

    def create_chat_prompt_template(self, section:str):
        agent_instructions = PROMPTS[section]
        parser = PydanticOutputParser(pydantic_object=schemas[section])
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
        ).partial(format_instructions=parser.get_format_instructions(), agent_instructions=agent_instructions)

        return prompt