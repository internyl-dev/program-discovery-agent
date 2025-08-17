
from langchain_core.output_parsers import PydanticOutputParser
from pprint import pp

from ..schemas import schemas

class ResponseParser:

    def parse_raw_response(self, raw_response, section:str):
        parser = PydanticOutputParser(pydantic_object=schemas[section])
        try:
            # The output is already a string, not a list with a text field
            raw_output = raw_response.get("output")
            
            # Remove the 'json' prefix if it exists
            if raw_output.startswith('json\n'):
                raw_output = raw_output[5:]  # Remove 'json\n'
            
            structured_response = self.parser.parse(raw_output)
            pp(structured_response)
            
        except Exception as e:
            print("Error parsing response", e)
            print("Raw Response - ", raw_response)
            print("Output content - ", raw_response.get("output"))